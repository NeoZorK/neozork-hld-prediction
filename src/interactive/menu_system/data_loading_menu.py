# -*- coding: utf-8 -*-
"""
Data Loading Menu for NeoZork Interactive ML Trading Strategy Development.

This module provides the data loading submenu with support for multiple data sources.
"""

from typing import Dict, Any, Optional
import time
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import colorama
from colorama import Fore, Back, Style
from .base_menu import BaseMenu
from src.interactive.data_management.file_analyzer import FileAnalyzer
from src.common.logger import print_error

class DataLoadingMenu(BaseMenu):
    """
    Data loading submenu with support for multiple data sources.
    
    Features:
    - CSV converted data loading
    - Raw parquet data loading
    - Indicators data loading
    - Cleaned data loading
    - Progress tracking with ETA
    """
    
    def __init__(self):
        """Initialize the data loading menu."""
        super().__init__()
        self.file_analyzer = FileAnalyzer()
        self.menu_items = {
            "1": {"title": "📁 CSV Converted (.parquet)", "handler": self._load_csv_converted},
            "2": {"title": "📊 Raw Parquet", "handler": self._load_raw_parquet},
            "3": {"title": "📈 Indicators", "handler": self._load_indicators},
            "4": {"title": "✨ Cleaned Data", "handler": self._load_cleaned_data},
            "0": {"title": "🔙 Back", "handler": None},
            "00": {"title": "🚪 Exit", "handler": self._exit_system}
        }
    
    def show_menu(self):
        """Display the data loading menu."""
        print(f"\n{Fore.YELLOW}📊 LOAD DATA")
        print(f"{Fore.CYAN}{'─'*50}")
        
        for key, item in self.menu_items.items():
            if key in ["0", "00"]:
                print(f"{Fore.RED}{key}. {item['title']}")
            else:
                print(f"{Fore.WHITE}{key}. {item['title']}")
        
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.YELLOW}💡 Choose data source to load into memory")
        print(f"{Fore.CYAN}{'─'*50}\n")
    
    def _load_csv_converted(self):
        """Load CSV converted data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}📁 CSV Converted Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_csv_converted_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "CSV Converted")
        
        # Display symbols found
        if analysis["symbols"]:
            print(f"\n{Fore.GREEN}📈 Available Symbols ({len(analysis['symbols'])}):")
            symbols_text = ", ".join(analysis["symbols"])
            print(f"{Fore.WHITE}  {symbols_text}")
        
        # Group files by symbol and sort
        if analysis["files_info"]:
            files_by_symbol = {}
            for filename, file_info in analysis["files_info"].items():
                # Extract symbol from filename
                symbol = self._extract_symbol_from_filename(filename)
                if symbol:
                    if symbol not in files_by_symbol:
                        files_by_symbol[symbol] = []
                    files_by_symbol[symbol].append((filename, file_info))
            
            # Sort symbols alphabetically
            sorted_symbols = sorted(files_by_symbol.keys())
            
            print(f"\n{Fore.YELLOW}📋 Files by Symbol ({len(sorted_symbols)} symbols):")
            print(f"{Fore.CYAN}{'─'*80}")
            
            for symbol in sorted_symbols:
                files = files_by_symbol[symbol]
                # Sort files by timeframe (M1, M5, M15, H1, H4, D1, W1, MN1)
                timeframe_order = {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 5, 'D1': 6, 'W1': 7, 'MN1': 8}
                files.sort(key=lambda x: timeframe_order.get(x[1]['timeframes'][0] if x[1]['timeframes'] else 'Unknown', 999))
                
                print(f"\n{Fore.GREEN}🔸 {symbol} ({len(files)} files):")
                
                # Display files in compact format
                for filename, file_info in files:
                    timeframe = file_info['timeframes'][0] if file_info['timeframes'] else 'Unknown'
                    size_mb = file_info['size_mb']
                    rows = file_info['rows']
                    start_date = file_info['start_date'][:10] if file_info['start_date'] != "No time data" else "No data"
                    end_date = file_info['end_date'][:10] if file_info['end_date'] != "No time data" else "No data"
                    
                    print(f"  {Fore.WHITE}{timeframe:>4} │ {size_mb:>6.1f}MB │ {rows:>8,} rows │ {start_date} to {end_date}")
        
        # Ask user to choose symbol and timeframe
        print(f"\n{Fore.GREEN}📊 Data Loading Configuration")
        print(f"{Fore.CYAN}{'─'*50}")
        
        # Get symbol from user (default: eurusd)
        symbol_input = input(f"{Fore.GREEN}Choose Symbol to load data into memory (e.g., 'eurusd') [default: eurusd]: {Style.RESET_ALL}").strip().upper()
        symbol = symbol_input if symbol_input else "EURUSD"
        
        # Check if symbol exists
        if symbol not in analysis["symbols"]:
            print(f"{Fore.RED}❌ Symbol '{symbol}' not found in available symbols.")
            print(f"{Fore.YELLOW}Available symbols: {', '.join(analysis['symbols'])}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Show available timeframes for this symbol
        symbol_files = [f for f in analysis["files_info"].items() if self._extract_symbol_from_filename(f[0]) == symbol]
        timeframes = []
        for filename, file_info in symbol_files:
            if file_info['timeframes'] and file_info['timeframes'][0] != 'No time data':
                timeframes.append(file_info['timeframes'][0])
        
        timeframes = sorted(list(set(timeframes)), key=lambda x: {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 5, 'D1': 6, 'W1': 7, 'MN1': 8}.get(x, 999))
        
        if not timeframes:
            print(f"{Fore.RED}❌ No valid timeframes found for symbol '{symbol}'")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Show timeframe selection menu
        print(f"\n{Fore.YELLOW}Choose Main Time Frame for {symbol}:")
        print(f"{Fore.CYAN}{'─'*40}")
        for i, tf in enumerate(timeframes, 1):
            print(f"{Fore.WHITE}{i}. {tf}")
        print(f"{Fore.CYAN}{'─'*40}")
        
        # Get timeframe choice (default: M1)
        try:
            choice_input = input(f"{Fore.GREEN}Enter choice (1-{len(timeframes)}) [default: 1 (M1)]: {Style.RESET_ALL}").strip()
            if not choice_input:
                # Default to M1 (first choice)
                choice_idx = 0
            else:
                choice_idx = int(choice_input) - 1
                
            if choice_idx < 0 or choice_idx >= len(timeframes):
                raise ValueError("Invalid choice")
            main_timeframe = timeframes[choice_idx]
        except (ValueError, IndexError):
            print(f"{Fore.RED}❌ Invalid choice. Exiting...")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        print(f"\n{Fore.GREEN}✅ Selected: {symbol} with main timeframe {main_timeframe}")
        
        # Load and save data
        self._load_and_save_symbol_data(symbol, main_timeframe, analysis)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_and_save_symbol_data(self, symbol: str, main_timeframe: str, analysis: Dict[str, Any]):
        """Load and save symbol data in ML-optimized format."""
        print(f"\n{Fore.YELLOW}🔄 Loading and processing {symbol} data...")
        
        try:
            from src.interactive.data_management import DataLoader
            import pandas as pd
            import numpy as np
            from pathlib import Path
            from datetime import datetime
            import time
            
            # Load data for the symbol
            loader = DataLoader()
            result = loader.load_csv_converted_data(symbol)
            
            if result["status"] != "success":
                print(f"{Fore.RED}❌ Error loading data: {result['message']}")
                return
            
            # Get all timeframes for this symbol
            symbol_files = [f for f in analysis["files_info"].items() if self._extract_symbol_from_filename(f[0]) == symbol]
            available_timeframes = []
            for filename, file_info in symbol_files:
                if file_info['timeframes'] and file_info['timeframes'][0] != 'No time data':
                    available_timeframes.append(file_info['timeframes'][0])
            
            available_timeframes = sorted(list(set(available_timeframes)), 
                                       key=lambda x: {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 5, 'D1': 6, 'W1': 7, 'MN1': 8}.get(x, 999))
            
            print(f"{Fore.GREEN}📊 Available timeframes: {', '.join(available_timeframes)}")
            print(f"{Fore.GREEN}🎯 Main timeframe: {main_timeframe}")
            
            # Create symbol directory
            symbol_dir = Path("data/cleaned_data") / symbol.lower()
            symbol_dir.mkdir(parents=True, exist_ok=True)
            
            # Process each timeframe
            processed_data = {}
            total_files = len(available_timeframes)
            
            for i, timeframe in enumerate(available_timeframes):
                progress = (i + 1) / total_files
                print(f"\r{Fore.CYAN}📊 Processing {timeframe}... [{int(progress*100):3d}%]", end="", flush=True)
                
                # Find the file for this timeframe
                timeframe_file = None
                for filename, file_info in symbol_files:
                    if file_info['timeframes'] and file_info['timeframes'][0] == timeframe:
                        timeframe_file = filename
                        break
                
                if not timeframe_file:
                    continue
                
                # Load the specific timeframe data
                file_path = Path("data/cache/csv_converted") / timeframe_file
                df = pd.read_parquet(file_path)
                
                # Standardize column names
                df = self._standardize_dataframe(df)
                
                # Add timeframe information
                df['timeframe'] = timeframe
                df['symbol'] = symbol.upper()
                
                # Store processed data
                processed_data[timeframe] = df
            
            print()  # New line after progress
            
            # Save data in ML-optimized format
            self._save_ml_optimized_data(symbol, main_timeframe, processed_data, symbol_dir)
            
            print(f"\n{Fore.GREEN}✅ Successfully saved {symbol} data to {symbol_dir}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error processing data: {e}")
            import traceback
            traceback.print_exc()
    
    def _standardize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize dataframe column names and structure."""
        # Create a copy to avoid modifying original
        df = df.copy()
        
        # Standardize column names
        column_mapping = {
            'Open': 'open',
            'High': 'high', 
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume',
            'Timestamp': 'timestamp',
            'Time': 'timestamp',
            'time': 'timestamp',
            'datetime': 'timestamp',
            'DateTime': 'timestamp'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Ensure timestamp is datetime
        if 'timestamp' in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.set_index('timestamp')
        
        # Ensure numeric columns are float
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sort by timestamp
        df = df.sort_index()
        
        return df
    
    def _save_ml_optimized_data(self, symbol: str, main_timeframe: str, processed_data: Dict[str, pd.DataFrame], symbol_dir: Path):
        """Save data in ML-optimized format."""
        from datetime import datetime
        import json
        
        # Create metadata
        metadata = {
            "symbol": symbol.upper(),
            "main_timeframe": main_timeframe,
            "available_timeframes": list(processed_data.keys()),
            "created_at": datetime.now().isoformat(),
            "total_timeframes": len(processed_data),
            "data_info": {}
        }
        
        # Save each timeframe
        for timeframe, df in processed_data.items():
            # Create timeframe directory
            tf_dir = symbol_dir / timeframe.lower()
            tf_dir.mkdir(parents=True, exist_ok=True)
            
            # Save as parquet (best for ML)
            parquet_file = tf_dir / f"{symbol.lower()}_{timeframe.lower()}.parquet"
            df.to_parquet(parquet_file, compression='snappy', index=True)
            
            # Save as feather for fast loading
            feather_file = tf_dir / f"{symbol.lower()}_{timeframe.lower()}.feather"
            df.reset_index().to_feather(feather_file)
            
            # Save metadata for this timeframe
            tf_metadata = {
                "timeframe": timeframe,
                "symbol": symbol.upper(),
                "rows": len(df),
                "columns": list(df.columns),
                "start_date": str(df.index.min()) if not df.empty else None,
                "end_date": str(df.index.max()) if not df.empty else None,
                "file_size_mb": parquet_file.stat().st_size / (1024 * 1024),
                "created_at": datetime.now().isoformat()
            }
            
            # Save timeframe metadata
            with open(tf_dir / "metadata.json", "w") as f:
                json.dump(tf_metadata, f, indent=2)
            
            # Update main metadata
            metadata["data_info"][timeframe] = tf_metadata
        
        # Save main metadata
        with open(symbol_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Create a summary file for quick access
        summary_data = {
            "symbol": symbol.upper(),
            "main_timeframe": main_timeframe,
            "timeframes": list(processed_data.keys()),
            "total_rows": sum(len(df) for df in processed_data.values()),
            "total_size_mb": sum(tf_dir.stat().st_size for tf_dir in symbol_dir.glob("*/") if tf_dir.is_dir()) / (1024 * 1024),
            "created_at": datetime.now().isoformat()
        }
        
        with open(symbol_dir / "summary.json", "w") as f:
            json.dump(summary_data, f, indent=2)
        
        # Create a Python loader script
        self._create_python_loader(symbol, main_timeframe, list(processed_data.keys()), symbol_dir)
    
    def _create_python_loader(self, symbol: str, main_timeframe: str, timeframes: list, symbol_dir: Path):
        """Create a Python loader script for easy data access."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        loader_script = f'''# -*- coding: utf-8 -*-
"""
Auto-generated data loader for {symbol.upper()}
Generated on: {current_time}

This script provides easy access to {symbol.upper()} data for ML/DL analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

class {symbol.upper()}DataLoader:
    """Data loader for {symbol.upper()} with multiple timeframes."""
    
    def __init__(self, data_dir: str = "data/cleaned_data/{symbol.lower()}"):
        self.data_dir = Path(data_dir)
        self.symbol = "{symbol.upper()}"
        self.main_timeframe = "{main_timeframe}"
        self.available_timeframes = {timeframes}
        
        # Load metadata
        with open(self.data_dir / "metadata.json", "r") as f:
            self.metadata = json.load(f)
    
    def load_timeframe(self, timeframe: str) -> pd.DataFrame:
        """Load data for specific timeframe."""
        if timeframe not in self.available_timeframes:
            raise ValueError(f"Timeframe {{timeframe}} not available. Available: {{self.available_timeframes}}")
        
        tf_dir = self.data_dir / timeframe.lower()
        parquet_file = tf_dir / f"{{self.symbol.lower()}}_{{timeframe.lower()}}.parquet"
        
        return pd.read_parquet(parquet_file)
    
    def load_all_timeframes(self) -> dict:
        """Load all available timeframes."""
        data = {{}}
        for tf in self.available_timeframes:
            data[tf] = self.load_timeframe(tf)
        return data
    
    def get_main_timeframe_data(self) -> pd.DataFrame:
        """Get data for main timeframe."""
        return self.load_timeframe(self.main_timeframe)
    
    def get_data_info(self) -> dict:
        """Get information about available data."""
        return self.metadata["data_info"]
    
    def get_summary(self) -> dict:
        """Get data summary."""
        with open(self.data_dir / "summary.json", "r") as f:
            return json.load(f)

# Example usage:
if __name__ == "__main__":
    loader = {symbol.upper()}DataLoader()
    
    # Load main timeframe
    main_data = loader.get_main_timeframe_data()
    print(f"Main timeframe data shape: {{main_data.shape}}")
    
    # Load all timeframes
    all_data = loader.load_all_timeframes()
    print(f"Available timeframes: {{list(all_data.keys())}}")
    
    # Get summary
    summary = loader.get_summary()
    print(f"Total rows: {{summary['total_rows']:,}}")
'''
        
        with open(symbol_dir / f"{symbol.lower()}_loader.py", "w") as f:
            f.write(loader_script)
    
    def _display_loaded_data(self, result: Dict[str, Any]):
        """Display loaded data information."""
        metadata = result["metadata"]
        data = result["data"]
        
        print(f"\n{Fore.GREEN}📊 Data Loaded Successfully!")
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.YELLOW}📈 Summary:")
        print(f"  • Total files: {metadata['total_files']}")
        print(f"  • Total size: {metadata['total_size_mb']} MB")
        print(f"  • Total rows: {metadata['total_rows']:,}")
        print(f"  • Symbols: {', '.join(metadata['symbols'])}")
        
        print(f"\n{Fore.YELLOW}📋 Detailed Information:")
        for symbol, info in data.items():
            print(f"\n{Fore.WHITE}🔸 {symbol}:")
            print(f"  • File: {info['file_path'].split('/')[-1]}")
            print(f"  • Size: {info['size_mb']} MB")
            print(f"  • Rows: {info['rows']:,}")
            print(f"  • Time range: {info['start_time']} to {info['end_time']}")
            print(f"  • Columns: {len(info['columns'])} ({', '.join(info['columns'][:5])}{'...' if len(info['columns']) > 5 else ''})")
    
    def _load_raw_parquet(self):
        """Load raw parquet data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}📊 Raw Parquet Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_raw_parquet_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "Raw Parquet")
        
        # Display sources found
        if analysis["sources"]:
            print(f"\n{Fore.GREEN}🏢 Available Sources:")
            sources_text = ", ".join(analysis["sources"])
            print(f"{Fore.WHITE}  {sources_text}")
        
        # Display symbols by source
        if analysis["symbols_by_source"]:
            print(f"\n{Fore.YELLOW}📈 Symbols by Source:")
            for source, symbols in analysis["symbols_by_source"].items():
                symbols_text = ", ".join(symbols)
                print(f"\n{Fore.WHITE}🔸 {source.upper()}:")
                print(f"  {symbols_text}")
        
        # Display files information
        if analysis["files_info"]:
            print(f"\n{Fore.YELLOW}📋 Files Information:")
            for filename, file_info in analysis["files_info"].items():
                print(f"\n{Fore.WHITE}🔸 {filename}:")
                print(f"  • Size: {file_info['size_mb']} MB")
                print(f"  • Rows: {file_info['rows']:,}")
                print(f"  • Date range: {file_info['start_date']} to {file_info['end_date']}")
                print(f"  • Timeframes: {', '.join(file_info['timeframes'][:3])}{'...' if len(file_info['timeframes']) > 3 else ''}")
        
        # Ask if user wants to load data
        load_data = input(f"\n{Fore.GREEN}Load data into memory? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if load_data == 'y':
            # Get symbol filter from user
            symbol_filter = input(f"{Fore.GREEN}Enter symbol filter (optional, e.g., 'btcusdt'): {Style.RESET_ALL}").strip()
            if not symbol_filter:
                symbol_filter = None
            
            # Load data
            from src.interactive.data_management import DataLoader
            loader = DataLoader()
            result = loader.load_raw_parquet_data(symbol_filter)
            
            if result["status"] == "success":
                self._display_loaded_data(result)
            else:
                print(f"{Fore.RED}❌ Error: {result['message']}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_indicators(self):
        """Load indicators data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}📈 Indicators Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_indicators_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "Indicators")
        
        # Display indicators found
        if analysis["indicators"]:
            print(f"\n{Fore.GREEN}📊 Available Indicators:")
            indicators_text = ", ".join(analysis["indicators"])
            print(f"{Fore.WHITE}  {indicators_text}")
        
        # Display subfolders information
        if analysis["subfolders_info"]:
            print(f"\n{Fore.YELLOW}📁 Subfolders Information:")
            for subdir, subfolder_info in analysis["subfolders_info"].items():
                print(f"\n{Fore.WHITE}🔸 {subdir.upper()}:")
                print(f"  • Files: {subfolder_info['file_count']}")
                print(f"  • Size: {subfolder_info['size_mb']} MB")
                print(f"  • Modified: {subfolder_info['modified']}")
                
                # Show files in this subfolder
                if subfolder_info.get("files_info"):
                    print(f"  • Files:")
                    for filename, file_info in subfolder_info["files_info"].items():
                        print(f"    - {filename}: {file_info['size_mb']} MB, {file_info['rows']:,} rows")
        
        # Ask if user wants to load data
        load_data = input(f"\n{Fore.GREEN}Load data into memory? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if load_data == 'y':
            # Get symbol filter from user
            symbol_filter = input(f"{Fore.GREEN}Enter symbol filter (optional, e.g., 'aapl'): {Style.RESET_ALL}").strip()
            if not symbol_filter:
                symbol_filter = None
            
            # Load data
            from src.interactive.data_management import DataLoader
            loader = DataLoader()
            result = loader.load_indicators_data(symbol_filter)
            
            if result["status"] == "success":
                self._display_loaded_data(result)
            else:
                print(f"{Fore.RED}❌ Error: {result['message']}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_cleaned_data(self):
        """Load cleaned data with detailed folder analysis and modern progress tracking."""
        print(f"\n{Fore.YELLOW}✨ Cleaned Data Analysis...")
        
        # Analyze cleaned data folder structure
        cleaned_dir = Path("data/cleaned_data")
        
        if not cleaned_dir.exists():
            print(f"{Fore.RED}❌ Cleaned data directory not found")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Get all symbol folders
        symbol_folders = [f for f in cleaned_dir.iterdir() if f.is_dir()]
        
        if not symbol_folders:
            print(f"{Fore.RED}❌ No symbol folders found in cleaned data")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        print(f"\n{Fore.GREEN}📈 Available Symbols ({len(symbol_folders)}):")
        print(f"{Fore.CYAN}{'─'*80}")
        
        # Analyze each symbol folder
        symbol_info = {}
        total_size = 0
        
        for symbol_folder in sorted(symbol_folders):
            symbol_name = symbol_folder.name.upper()
            symbol_info[symbol_name] = self._analyze_symbol_folder(symbol_folder)
            total_size += symbol_info[symbol_name]['total_size_mb']
        
        # Display symbol information in a modern table format
        print(f"{Fore.WHITE}{'Symbol':<12} {'Size (MB)':<10} {'Files':<6} {'Timeframes':<20} {'Start Date':<12} {'End Date':<12}")
        print(f"{Fore.CYAN}{'─'*80}")
        
        for symbol_name, info in symbol_info.items():
            timeframes_str = ', '.join(info['timeframes'][:3])
            if len(info['timeframes']) > 3:
                timeframes_str += f" +{len(info['timeframes'])-3} more"
            
            start_date = info['start_date'][:10] if info['start_date'] != "No data" else "No data"
            end_date = info['end_date'][:10] if info['end_date'] != "No data" else "No data"
            
            print(f"{Fore.WHITE}{symbol_name:<12} {info['total_size_mb']:<10.1f} {info['file_count']:<6} {timeframes_str:<20} {start_date:<12} {end_date:<12}")
        
        print(f"{Fore.CYAN}{'─'*80}")
        print(f"{Fore.YELLOW}Total: {len(symbol_folders)} symbols, {total_size:.1f} MB")
        
        # Ask user to choose symbol
        print(f"\n{Fore.GREEN}📊 Choose Symbol to Load into Memory")
        print(f"{Fore.CYAN}{'─'*50}")
        
        symbol_choice = input(f"{Fore.GREEN}Enter symbol name (e.g., 'eurusd') [default: eurusd]: {Style.RESET_ALL}").strip().lower()
        if not symbol_choice:
            symbol_choice = "eurusd"
        
        symbol_choice_upper = symbol_choice.upper()
        
        if symbol_choice_upper not in symbol_info:
            print(f"{Fore.RED}❌ Symbol '{symbol_choice_upper}' not found")
            print(f"{Fore.YELLOW}Available symbols: {', '.join(symbol_info.keys())}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Show available timeframes for selected symbol
        selected_info = symbol_info[symbol_choice_upper]
        print(f"\n{Fore.GREEN}📈 {symbol_choice_upper} - Available Timeframes:")
        print(f"{Fore.CYAN}{'─'*40}")
        
        for i, tf in enumerate(selected_info['timeframes'], 1):
            tf_info = selected_info['timeframe_details'][tf]
            print(f"{Fore.WHITE}{i:2d}. {tf:<4} │ {tf_info['size_mb']:>6.1f}MB │ {tf_info['rows']:>8,} rows │ {tf_info['start_date'][:10]} to {tf_info['end_date'][:10]}")
        
        print(f"{Fore.CYAN}{'─'*40}")
        
        # Ask for timeframe choice
        try:
            tf_choice = input(f"{Fore.GREEN}Choose main timeframe (1-{len(selected_info['timeframes'])}) [default: 1 (M1)]: {Style.RESET_ALL}").strip()
            if not tf_choice:
                tf_choice = "1"
            
            tf_idx = int(tf_choice) - 1
            if tf_idx < 0 or tf_idx >= len(selected_info['timeframes']):
                raise ValueError("Invalid choice")
            
            main_timeframe = selected_info['timeframes'][tf_idx]
        except (ValueError, IndexError):
            print(f"{Fore.RED}❌ Invalid choice. Using M1 as default.")
            main_timeframe = "M1"
        
        print(f"\n{Fore.GREEN}✅ Selected: {symbol_choice_upper} with main timeframe {main_timeframe}")
        
        # Load data with modern progress tracking
        self._load_symbol_data_with_progress(symbol_choice, main_timeframe, selected_info)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _display_folder_info(self, folder_info: Dict[str, Any], folder_name: str):
        """Display detailed folder information."""
        print(f"\n{Fore.CYAN}📁 {folder_name} Folder Information:")
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.WHITE}  • Path: {folder_info['path']}")
        print(f"{Fore.WHITE}  • Files: {folder_info['file_count']}")
        print(f"{Fore.WHITE}  • Size: {folder_info['size_mb']} MB")
        print(f"{Fore.WHITE}  • Modified: {folder_info['modified']}")
        print(f"{Fore.CYAN}{'─'*50}")
    
    def _analyze_symbol_folder(self, symbol_folder: Path) -> Dict[str, Any]:
        """Analyze a symbol folder for detailed information."""
        try:
            # Get all timeframe folders
            timeframe_folders = [f for f in symbol_folder.iterdir() if f.is_dir() and f.name != '__pycache__']
            
            timeframes = []
            timeframe_details = {}
            total_size_mb = 0
            total_files = 0
            start_date = "No data"
            end_date = "No data"
            
            for tf_folder in sorted(timeframe_folders):
                tf_name = tf_folder.name.upper()
                timeframes.append(tf_name)
                
                # Get parquet file
                parquet_file = tf_folder / f"{symbol_folder.name}_{tf_name.lower()}.parquet"
                if parquet_file.exists():
                    # Get file size
                    file_size_mb = parquet_file.stat().st_size / (1024 * 1024)
                    total_size_mb += file_size_mb
                    total_files += 1
                    
                    # Load metadata if available
                    metadata_file = tf_folder / "metadata.json"
                    if metadata_file.exists():
                        try:
                            import json
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                            
                            tf_info = {
                                'size_mb': file_size_mb,
                                'rows': metadata.get('rows', 0),
                                'start_date': metadata.get('start_date', 'No data'),
                                'end_date': metadata.get('end_date', 'No data'),
                                'columns': metadata.get('columns', [])
                            }
                            
                            # Update overall start/end dates
                            if tf_info['start_date'] != 'No data' and start_date == "No data":
                                start_date = tf_info['start_date']
                            elif tf_info['start_date'] != 'No data' and tf_info['start_date'] < start_date:
                                start_date = tf_info['start_date']
                            
                            if tf_info['end_date'] != 'No data' and end_date == "No data":
                                end_date = tf_info['end_date']
                            elif tf_info['end_date'] != 'No data' and tf_info['end_date'] > end_date:
                                end_date = tf_info['end_date']
                                
                        except Exception as e:
                            print_error(f"Error reading metadata for {tf_name}: {e}")
                            tf_info = {
                                'size_mb': file_size_mb,
                                'rows': 0,
                                'start_date': 'No data',
                                'end_date': 'No data',
                                'columns': []
                            }
                    else:
                        tf_info = {
                            'size_mb': file_size_mb,
                            'rows': 0,
                            'start_date': 'No data',
                            'end_date': 'No data',
                            'columns': []
                        }
                    
                    timeframe_details[tf_name] = tf_info
            
            return {
                'timeframes': timeframes,
                'timeframe_details': timeframe_details,
                'total_size_mb': total_size_mb,
                'file_count': total_files,
                'start_date': start_date,
                'end_date': end_date
            }
            
        except Exception as e:
            print_error(f"Error analyzing symbol folder {symbol_folder}: {e}")
            return {
                'timeframes': [],
                'timeframe_details': {},
                'total_size_mb': 0,
                'file_count': 0,
                'start_date': 'No data',
                'end_date': 'No data'
            }
    
    def _load_symbol_data_with_progress(self, symbol: str, main_timeframe: str, symbol_info: Dict[str, Any]):
        """Load symbol data with modern progress tracking and memory usage display."""
        print(f"\n{Fore.YELLOW}🔄 Loading {symbol.upper()} data into memory...")
        
        try:
            import psutil
            import time
            from pathlib import Path
            import pandas as pd
            import numpy as np
            
            # Get initial memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
            
            # Load all timeframes
            loaded_data = {}
            total_timeframes = len(symbol_info['timeframes'])
            
            print(f"{Fore.CYAN}📊 Loading {total_timeframes} timeframes...")
            
            start_time = time.time()
            
            for i, timeframe in enumerate(symbol_info['timeframes']):
                # Calculate progress
                progress = (i + 1) / total_timeframes
                
                # Calculate ETA
                current_time = time.time()
                elapsed_time = current_time - start_time
                if i > 0:
                    avg_time_per_tf = elapsed_time / i
                    remaining_tfs = total_timeframes - i
                    eta_seconds = remaining_tfs * avg_time_per_tf
                    eta_str = self._format_time(eta_seconds)
                else:
                    eta_str = "Calculating..."
                
                # Calculate speed
                if elapsed_time > 0:
                    speed = f"{i / elapsed_time:.1f} tf/s"
                else:
                    speed = "Starting..."
                
                # Show progress
                self._show_loading_progress(f"Loading {timeframe}", progress, eta_str, speed)
                
                # Load timeframe data
                tf_folder = Path(f"data/cleaned_data/{symbol.lower()}/{timeframe.lower()}")
                parquet_file = tf_folder / f"{symbol.lower()}_{timeframe.lower()}.parquet"
                
                if parquet_file.exists():
                    try:
                        df = pd.read_parquet(parquet_file)
                        loaded_data[timeframe] = df
                    except Exception as e:
                        print_error(f"Error loading {timeframe}: {e}")
                        continue
                else:
                    print_error(f"File not found: {parquet_file}")
                    continue
            
            # Final progress display
            total_time = time.time() - start_time
            self._show_loading_progress(f"Completed loading {total_timeframes} timeframes", 1.0, "", f"{total_timeframes / total_time:.1f} tf/s")
            
            # Get final memory usage
            final_memory = process.memory_info().rss / (1024 * 1024)  # MB
            memory_used = final_memory - initial_memory
            
            # Display loading results
            print(f"\n{Fore.GREEN}✅ Data loaded successfully!")
            print(f"{Fore.CYAN}{'─'*60}")
            print(f"{Fore.YELLOW}📊 Loading Summary:")
            print(f"  • Symbol: {symbol.upper()}")
            print(f"  • Main Timeframe: {main_timeframe}")
            print(f"  • Timeframes loaded: {len(loaded_data)}")
            print(f"  • Total rows: {sum(len(df) for df in loaded_data.values()):,}")
            print(f"  • Loading time: {total_time:.2f} seconds")
            print(f"  • Memory used: {memory_used:.1f} MB")
            print(f"  • Total memory: {final_memory:.1f} MB")
            
            # Display timeframe details
            print(f"\n{Fore.YELLOW}📋 Timeframe Details:")
            for tf, df in loaded_data.items():
                tf_info = symbol_info['timeframe_details'][tf]
                print(f"  • {tf:<4}: {len(df):>8,} rows, {tf_info['size_mb']:>6.1f} MB, {tf_info['start_date'][:10]} to {tf_info['end_date'][:10]}")
            
            # Create MTF (Multi-Timeframe) data structure for ML
            print(f"\n{Fore.YELLOW}🔧 Creating MTF data structure for ML...")
            mtf_data = self._create_mtf_structure(loaded_data, main_timeframe)
            
            # Save loaded data for future use
            self._save_loaded_data(symbol, main_timeframe, loaded_data, mtf_data)
            
            print(f"\n{Fore.GREEN}🎯 MTF data structure created and saved!")
            print(f"  • Main timeframe: {main_timeframe}")
            print(f"  • Available timeframes: {', '.join(loaded_data.keys())}")
            print(f"  • Data shape: {mtf_data['main_data'].shape if 'main_data' in mtf_data else 'N/A'}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_mtf_structure(self, loaded_data: Dict[str, pd.DataFrame], main_timeframe: str) -> Dict[str, Any]:
        """Create Multi-Timeframe data structure optimized for ML."""
        try:
            mtf_data = {
                'main_timeframe': main_timeframe,
                'timeframes': list(loaded_data.keys()),
                'main_data': loaded_data.get(main_timeframe, pd.DataFrame()),
                'timeframe_data': loaded_data,
                'metadata': {
                    'created_at': pd.Timestamp.now().isoformat(),
                    'total_rows': sum(len(df) for df in loaded_data.values()),
                    'timeframe_counts': {tf: len(df) for tf, df in loaded_data.items()}
                }
            }
            
            # Add cross-timeframe features if multiple timeframes available
            if len(loaded_data) > 1:
                mtf_data['cross_timeframe_features'] = self._create_cross_timeframe_features(loaded_data, main_timeframe)
            
            return mtf_data
            
        except Exception as e:
            print_error(f"Error creating MTF structure: {e}")
            return {'error': str(e)}
    
    def _create_cross_timeframe_features(self, loaded_data: Dict[str, pd.DataFrame], main_timeframe: str) -> Dict[str, Any]:
        """Create cross-timeframe features for ML."""
        try:
            main_df = loaded_data[main_timeframe]
            cross_features = {}
            
            # Add features from higher timeframes
            for tf, df in loaded_data.items():
                if tf != main_timeframe:
                    # Resample to main timeframe frequency
                    resampled = df.resample('1min').ffill()  # Forward fill to 1-minute frequency
                    cross_features[tf] = resampled
            
            return cross_features
            
        except Exception as e:
            print_error(f"Error creating cross-timeframe features: {e}")
            return {}
    
    def _save_loaded_data(self, symbol: str, main_timeframe: str, loaded_data: Dict[str, pd.DataFrame], mtf_data: Dict[str, Any]):
        """Save loaded data for future use."""
        try:
            import pickle
            from pathlib import Path
            import json
            
            # Create cache directory
            cache_dir = Path("data/cache/loaded_data")
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Save MTF data structure
            mtf_file = cache_dir / f"{symbol.lower()}_mtf_{main_timeframe.lower()}.pkl"
            with open(mtf_file, 'wb') as f:
                pickle.dump(mtf_data, f)
            
            # Save metadata
            metadata = {
                'symbol': symbol.upper(),
                'main_timeframe': main_timeframe,
                'timeframes': list(loaded_data.keys()),
                'total_rows': sum(len(df) for df in loaded_data.values()),
                'created_at': pd.Timestamp.now().isoformat(),
                'file_path': str(mtf_file)
            }
            
            metadata_file = cache_dir / f"{symbol.lower()}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"{Fore.GREEN}💾 Data saved to: {mtf_file}")
            
        except Exception as e:
            print_error(f"Error saving loaded data: {e}")
    
    def _show_loading_progress(self, message: str, progress: float = 0.0, eta: str = "", speed: str = ""):
        """Show modern loading progress with ETA and speed."""
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        # Create progress display
        progress_display = f"{Fore.CYAN}🔄 {message}"
        bar_display = f"{Fore.GREEN}[{bar}]{Fore.CYAN}"
        percentage_display = f"{Fore.YELLOW}{percentage:3d}%"
        
        # Add ETA and speed if available
        extra_info = ""
        if eta:
            extra_info += f" {Fore.MAGENTA}ETA: {eta}"
        if speed:
            extra_info += f" {Fore.BLUE}Speed: {speed}"
        
        # Combine all parts
        full_display = f"\r{progress_display} {bar_display} {percentage_display}{extra_info}{Style.RESET_ALL}"
        
        # Ensure the line is long enough to clear previous content
        terminal_width = 120
        if len(full_display) < terminal_width:
            full_display += " " * (terminal_width - len(full_display))
        
        print(full_display, end="", flush=True)
        
        if progress >= 1.0:
            print()  # New line when complete
    
    def _format_time(self, seconds: float) -> str:
        """Format time in seconds to human readable format."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def _extract_symbol_from_filename(self, filename: str) -> Optional[str]:
        """Extract symbol from filename."""
        try:
            # Remove extension
            name = filename.split('.')[0]
            
            # Look for patterns like CSVExport_SYMBOL_PERIOD_...
            if "CSVExport_" in name:
                parts = name.split("_")
                if len(parts) >= 2:
                    return parts[1].upper()
            
            # Look for patterns like cleaned_csv_converted_SYMBOL_...
            if "cleaned_csv_converted_" in name:
                parts = name.split("_")
                if len(parts) >= 4:
                    return parts[3].upper()
            
            # Look for patterns like SYMBOL_PERIOD_...
            if "_PERIOD_" in name:
                parts = name.split("_")
                if len(parts) >= 2:
                    return parts[0].upper()
            
            return None
        except Exception as e:
            print_error(f"Error extracting symbol from {filename}: {e}")
            return None
