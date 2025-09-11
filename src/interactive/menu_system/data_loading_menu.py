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
        
        # Get symbol from user
        symbol = input(f"{Fore.GREEN}Choose Symbol to load data into memory (e.g., 'eurusd'): {Style.RESET_ALL}").strip().upper()
        if not symbol:
            print(f"{Fore.RED}❌ No symbol provided. Exiting...")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
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
        
        # Get timeframe choice
        try:
            choice = input(f"{Fore.GREEN}Enter choice (1-{len(timeframes)}): {Style.RESET_ALL}").strip()
            choice_idx = int(choice) - 1
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
        """Load cleaned data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}✨ Cleaned Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_cleaned_data_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "Cleaned Data")
        
        # Display symbols found
        if analysis["symbols"]:
            print(f"\n{Fore.GREEN}📈 Available Symbols:")
            symbols_text = ", ".join(analysis["symbols"])
            print(f"{Fore.WHITE}  {symbols_text}")
        
        # Display save dates
        if analysis["save_dates"]:
            print(f"\n{Fore.GREEN}📅 Save Dates:")
            dates_text = ", ".join(analysis["save_dates"])
            print(f"{Fore.WHITE}  {dates_text}")
        
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
            symbol_filter = input(f"{Fore.GREEN}Enter symbol filter (optional, e.g., 'eurusd'): {Style.RESET_ALL}").strip()
            if not symbol_filter:
                symbol_filter = None
            
            # Load data
            from src.interactive.data_management import DataLoader
            loader = DataLoader()
            result = loader.load_cleaned_data(symbol_filter)
            
            if result["status"] == "success":
                self._display_loaded_data(result)
            else:
                print(f"{Fore.RED}❌ Error: {result['message']}")
        
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
