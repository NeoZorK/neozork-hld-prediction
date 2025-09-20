# -*- coding: utf-8 -*-
"""
Data Loading Menu for NeoZork Interactive ML Trading Strategy Development.

This module provides the data loading submenu with support for multiple data sources.
"""

from typing import Dict, Any, Optional, Tuple, List
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
        
        # Load and save data with MTF structure
        self._load_and_save_symbol_data_with_mtf(symbol, main_timeframe, analysis)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_and_save_symbol_data_with_mtf(self, symbol: str, main_timeframe: str, analysis: Dict[str, Any]):
        """Load and save symbol data with immediate MTF structure creation."""
        print(f"\n{Fore.YELLOW}🔄 Loading and processing {symbol} data...")
        
        try:
            from .data_loading import DataLoader, SymbolDisplay
            import pandas as pd
            import numpy as np
            from pathlib import Path
            from datetime import datetime
            import time
            
            # Load data for the symbol from CSV converted files
            print(f"{Fore.CYAN}📊 Loading data from CSV converted files...")
            
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
            
            # DataLoader will create the necessary directories
            
            # Process each timeframe
            processed_data = {}
            total_files = len(available_timeframes)
            
            print(f"\n{Fore.YELLOW}🔄 Processing timeframes...")
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
                
                # Store source path for data source determination
                df.attrs['source_path'] = str(file_path)
                
                # Store processed data
                processed_data[timeframe] = df
            
            print()  # New line after progress
            
            # Determine data source from the first loaded file
            data_source = 'csv'  # Default for CSV converted data
            if processed_data:
                first_tf = list(processed_data.keys())[0]
                first_df = processed_data[first_tf]
                if hasattr(first_df, 'attrs') and 'source_path' in first_df.attrs:
                    # Import DataLoader to use its method
                    from .data_loading import DataLoader
                    loader = DataLoader()
                    data_source = loader._determine_data_source(first_df.attrs['source_path'])
            
            print(f"{Fore.GREEN}📊 Data source detected: {data_source}")
            
            # Skip saving individual timeframe data - only save MTF structure
            print(f"{Fore.YELLOW}💡 Skipping individual timeframe saving - only MTF structure will be saved")
            
            # Create MTF structure immediately with progress tracking
            print(f"\n{Fore.YELLOW}🔧 Creating MTF data structure for ML...")
            mtf_data = self._create_mtf_structure_with_progress(processed_data, main_timeframe, symbol)
            
            # Save MTF structure with progress tracking and data source
            self._save_mtf_structure_with_progress(symbol, mtf_data, data_source)
            
            # Get the actual save directory from DataLoader
            from .data_loading import DataLoader
            loader = DataLoader()
            source_dir = loader.mtf_dir / data_source
            symbol_mtf_dir = source_dir / symbol.lower()
            
            print(f"\n{Fore.GREEN}✅ Successfully saved {symbol} data to {symbol_mtf_dir}")
            print(f"{Fore.GREEN}🎯 MTF structure created and saved for ML!")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error processing data: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_mtf_structure_with_progress(self, processed_data: Dict[str, pd.DataFrame], main_timeframe: str, symbol: str) -> Dict[str, Any]:
        """Create MTF structure from processed data with modern progress tracking."""
        try:
            import time
            from .data_loading import DataLoader
            
            # Calculate total steps for progress tracking
            total_steps = 3  # Main data + cross features + metadata
            if len(processed_data) > 1:
                total_steps += len(processed_data) - 1  # Additional cross-timeframe features
            
            current_step = 0
            start_time = time.time()
            
            # Step 1: Create main MTF data structure
            current_step += 1
            progress = current_step / total_steps
            self._show_mtf_progress("Creating main data structure", progress, start_time)
            
            mtf_data = {
                'symbol': symbol.upper(),
                'main_timeframe': main_timeframe,
                'timeframes': list(processed_data.keys()),
                'main_data': processed_data.get(main_timeframe, pd.DataFrame()),
                'timeframe_data': processed_data,
                'metadata': {
                    'created_at': pd.Timestamp.now().isoformat(),
                    'total_rows': sum(len(df) for df in processed_data.values()),
                    'timeframe_counts': {tf: len(df) for tf, df in processed_data.items()}
                }
            }
            
            # Step 2: Add cross-timeframe features if multiple timeframes available
            if len(processed_data) > 1:
                current_step += 1
                progress = current_step / total_steps
                self._show_mtf_progress("Creating cross-timeframe features", progress, start_time)
                
                mtf_data['cross_timeframe_features'] = self._create_cross_timeframe_features_with_progress(
                    processed_data, main_timeframe, start_time, current_step, total_steps)
            
            # Step 3: Finalize metadata
            current_step += 1
            progress = current_step / total_steps
            self._show_mtf_progress("Finalizing MTF structure", progress, start_time)
            
            # Final progress display
            total_time = time.time() - start_time
            self._show_mtf_progress("MTF structure created successfully", 1.0, start_time)
            
            return mtf_data
            
        except Exception as e:
            print_error(f"Error creating MTF structure: {e}")
            return {'error': str(e)}
    
    def _create_mtf_structure_from_processed_data(self, processed_data: Dict[str, pd.DataFrame], main_timeframe: str, symbol: str) -> Dict[str, Any]:
        """Create MTF structure from processed data (legacy method)."""
        try:
            from .data_loading import DataLoader
            
            # Create MTF data structure
            mtf_data = {
                'symbol': symbol.upper(),
                'main_timeframe': main_timeframe,
                'timeframes': list(processed_data.keys()),
                'main_data': processed_data.get(main_timeframe, pd.DataFrame()),
                'timeframe_data': processed_data,
                'metadata': {
                    'created_at': pd.Timestamp.now().isoformat(),
                    'total_rows': sum(len(df) for df in processed_data.values()),
                    'timeframe_counts': {tf: len(df) for tf, df in processed_data.items()}
                }
            }
            
            # Add cross-timeframe features if multiple timeframes available
            if len(processed_data) > 1:
                mtf_data['cross_timeframe_features'] = self._create_cross_timeframe_features(processed_data, main_timeframe)
            
            return mtf_data
            
        except Exception as e:
            print_error(f"Error creating MTF structure: {e}")
            return {'error': str(e)}
    
    def _create_cross_timeframe_features_with_progress(self, processed_data: Dict[str, pd.DataFrame], main_timeframe: str, start_time: float, current_step: int, total_steps: int) -> Dict[str, Any]:
        """Create cross-timeframe features for ML with progress tracking."""
        try:
            main_df = processed_data[main_timeframe]
            cross_features = {}
            
            # Get timeframes to process
            timeframes_to_process = [tf for tf in processed_data.keys() if tf != main_timeframe]
            
            # Add features from higher timeframes
            for i, tf in enumerate(timeframes_to_process):
                # Update progress
                step_progress = (current_step + i) / total_steps
                self._show_mtf_progress(f"Processing {tf} cross-features", step_progress, start_time)
                
                df = processed_data[tf]
                # Resample to main timeframe frequency
                resampled = df.resample('1min').ffill()  # Forward fill to 1-minute frequency
                cross_features[tf] = resampled
            
            return cross_features
            
        except Exception as e:
            print_error(f"Error creating cross-timeframe features: {e}")
            return {}
    
    def _create_cross_timeframe_features(self, processed_data: Dict[str, pd.DataFrame], main_timeframe: str) -> Dict[str, Any]:
        """Create cross-timeframe features for ML (legacy method)."""
        try:
            main_df = processed_data[main_timeframe]
            cross_features = {}
            
            # Add features from higher timeframes
            for tf, df in processed_data.items():
                if tf != main_timeframe:
                    # Resample to main timeframe frequency
                    resampled = df.resample('1min').ffill()  # Forward fill to 1-minute frequency
                    cross_features[tf] = resampled
            
            return cross_features
            
        except Exception as e:
            print_error(f"Error creating cross-timeframe features: {e}")
            return {}
    
    def _show_mtf_progress(self, message: str, progress: float, start_time: float):
        """Show modern MTF progress with ETA and percentage."""
        import time
        
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        # Calculate ETA
        current_time = time.time()
        elapsed_time = current_time - start_time
        if progress > 0:
            eta_seconds = (elapsed_time / progress) - elapsed_time
            eta_str = self._format_time(eta_seconds)
        else:
            eta_str = "Calculating..."
        
        # Calculate speed
        if elapsed_time > 0:
            speed = f"{progress / elapsed_time:.1f} steps/s"
        else:
            speed = "Starting..."
        
        # Create progress display
        progress_display = f"{Fore.CYAN}🔧 {message}"
        bar_display = f"{Fore.GREEN}[{bar}]{Fore.CYAN}"
        percentage_display = f"{Fore.YELLOW}{percentage:3d}%"
        
        # Add ETA and speed
        extra_info = f" {Fore.MAGENTA}ETA: {eta_str} {Fore.BLUE}Speed: {speed}"
        
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
    
    def _show_indicators_progress(self, message: str, progress: float, start_time: float, 
                                 current_step: str = "", total_steps: int = 0):
        """Show modern indicators progress with ETA and percentage."""
        import time
        
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        # Calculate ETA
        current_time = time.time()
        elapsed_time = current_time - start_time
        if progress > 0 and progress < 1.0:
            eta_seconds = (elapsed_time / progress) - elapsed_time
            eta_str = self._format_time(eta_seconds)
        elif progress >= 1.0:
            eta_str = "Complete"
        else:
            eta_str = "Calculating..."
        
        # Calculate speed
        if elapsed_time > 0 and progress > 0:
            speed = f"{progress / elapsed_time:.1f} ops/s"
        else:
            speed = "Starting..."
        
        # Create progress display
        progress_display = f"{Fore.CYAN}📈 {message}"
        bar_display = f"{Fore.GREEN}[{bar}]{Fore.CYAN}"
        percentage_display = f"{Fore.YELLOW}{percentage:3d}%"
        
        # Add step information if available
        step_info = ""
        if current_step and total_steps > 0:
            step_info = f" {Fore.WHITE}({current_step}/{total_steps})"
        
        # Add ETA and speed
        extra_info = f" {Fore.MAGENTA}ETA: {eta_str} {Fore.BLUE}Speed: {speed}"
        
        # Combine all parts
        full_display = f"\r{progress_display} {bar_display} {percentage_display}{step_info}{extra_info}{Style.RESET_ALL}"
        
        # Ensure the line is long enough to clear previous content
        terminal_width = 120
        if len(full_display) < terminal_width:
            full_display += " " * (terminal_width - len(full_display))
        
        print(full_display, end="", flush=True)
        
        if progress >= 1.0:
            print()  # New line when complete
    
    def _show_unified_progress(self, message: str, progress: float, start_time: float):
        """Show unified progress bar that updates in single line."""
        import time
        
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        # Calculate ETA
        current_time = time.time()
        elapsed_time = current_time - start_time
        if progress > 0 and progress < 1.0:
            eta_seconds = (elapsed_time / progress) - elapsed_time
            eta_str = self._format_time(eta_seconds)
        elif progress >= 1.0:
            eta_str = "Complete"
        else:
            eta_str = "Calculating..."
        
        # Calculate speed
        if elapsed_time > 0 and progress > 0:
            speed = f"{progress / elapsed_time:.1f} ops/s"
        else:
            speed = "Starting..."
        
        # Create progress display
        progress_display = f"{Fore.CYAN}📈 {message}"
        bar_display = f"{Fore.GREEN}[{bar}]{Fore.CYAN}"
        percentage_display = f"{Fore.YELLOW}{percentage:3d}%"
        
        # Add ETA and speed
        extra_info = f" {Fore.MAGENTA}ETA: {eta_str} {Fore.BLUE}Speed: {speed}"
        
        # Combine all parts
        full_display = f"\r{progress_display} {bar_display} {percentage_display}{extra_info}{Style.RESET_ALL}"
        
        # Ensure the line is long enough to clear previous content
        terminal_width = 120
        if len(full_display) < terminal_width:
            full_display += " " * (terminal_width - len(full_display))
        
        print(full_display, end="", flush=True)
        
        # Only print new line when complete
        if progress >= 1.0:
            print()  # New line when complete
    
    def _save_mtf_structure_with_progress(self, symbol: str, mtf_data: Dict[str, Any], data_source: str = 'unknown'):
        """Save MTF structure in ML-optimized format with progress tracking."""
        try:
            import time
            from .data_loading import DataLoader
            import json
            
            start_time = time.time()
            
            # Step 1: Prepare data
            self._show_mtf_progress("Preparing MTF data for saving", 0.1, start_time)
            
            # Use DataLoader to save MTF structure
            loader = DataLoader()
            
            # Create symbol info for DataLoader
            symbol_info = {
                'timeframes': mtf_data['timeframes'],
                'timeframe_details': {}
            }
            
            # Fill timeframe details
            for tf in mtf_data['timeframes']:
                df = mtf_data['timeframe_data'][tf]
                symbol_info['timeframe_details'][tf] = {
                    'size_mb': 0,  # Will be calculated by DataLoader
                    'rows': len(df),
                    'start_date': str(df.index.min()) if not df.empty else 'No data',
                    'end_date': str(df.index.max()) if not df.empty else 'No data',
                    'columns': list(df.columns)
                }
            
            # Step 2: Save main data
            self._show_mtf_progress("Saving main timeframe data", 0.3, start_time)
            
            # Step 3: Save cross-timeframe features
            self._show_mtf_progress("Saving cross-timeframe features", 0.6, start_time)
            
            # Step 4: Save metadata and create loader
            self._show_mtf_progress("Saving metadata and creating ML loader", 0.8, start_time)
            
            # Save using DataLoader's method with data source
            loader._save_loaded_data(symbol, mtf_data['timeframe_data'], mtf_data, data_source)
            
            # Final step
            self._show_mtf_progress("MTF structure saved successfully", 1.0, start_time)
            
        except Exception as e:
            print_error(f"Error saving MTF structure: {e}")
    
    def _save_mtf_structure(self, symbol: str, mtf_data: Dict[str, Any]):
        """Save MTF structure in ML-optimized format (legacy method)."""
        try:
            from .data_loading import DataLoader
            import json
            
            # Use DataLoader to save MTF structure
            loader = DataLoader()
            
            # Create symbol info for DataLoader
            symbol_info = {
                'timeframes': mtf_data['timeframes'],
                'timeframe_details': {}
            }
            
            # Fill timeframe details
            for tf in mtf_data['timeframes']:
                df = mtf_data['timeframe_data'][tf]
                symbol_info['timeframe_details'][tf] = {
                    'size_mb': 0,  # Will be calculated by DataLoader
                    'rows': len(df),
                    'start_date': str(df.index.min()) if not df.empty else 'No data',
                    'end_date': str(df.index.max()) if not df.empty else 'No data',
                    'columns': list(df.columns)
                }
            
            # Save using DataLoader's method with data source
            loader._save_loaded_data(symbol, mtf_data['timeframe_data'], mtf_data, 'unknown')
            
        except Exception as e:
            print_error(f"Error saving MTF structure: {e}")
    
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
            
            # DataLoader will create the necessary directories
            
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
            
            # Skip saving individual timeframe data - only save MTF structure
            print(f"{Fore.YELLOW}💡 Skipping individual timeframe saving - only MTF structure will be saved")
            
            print(f"\n{Fore.GREEN}✅ Successfully processed {symbol} data (MTF structure only)")
            
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
        """Load raw parquet data with detailed folder analysis and MTF structure creation."""
        print(f"\n{Fore.YELLOW}📊 Raw Parquet Data Analysis...")
        
        # Import raw parquet modules
        from src.interactive.data_management.raw_parquet import (
            RawParquetAnalyzer, RawParquetLoader, RawParquetProcessor, RawParquetMTFCreator
        )
        
        # Initialize components
        analyzer = RawParquetAnalyzer()
        loader = RawParquetLoader()
        processor = RawParquetProcessor()
        mtf_creator = RawParquetMTFCreator()
        
        # Analyze folder first
        analysis = analyzer.analyze_raw_parquet_folder()
        
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
        
        # Group files by symbol and source
        if analysis["files_info"]:
            files_by_symbol = {}
            for filename, file_info in analysis["files_info"].items():
                # Extract source and symbol from filename
                source, symbol = self._extract_source_and_symbol_from_filename(filename)
                if source and symbol:
                    key = f"{source}_{symbol}"
                    if key not in files_by_symbol:
                        files_by_symbol[key] = []
                    files_by_symbol[key].append((filename, file_info))
            
            # Sort symbols alphabetically
            sorted_symbols = sorted(files_by_symbol.keys())
            
            print(f"\n{Fore.YELLOW}📋 Files by Symbol ({len(sorted_symbols)} symbols):")
            print(f"{Fore.CYAN}{'─'*80}")
            
            for symbol_key in sorted_symbols:
                files = files_by_symbol[symbol_key]
                source, symbol = symbol_key.split('_', 1)
                
                # Sort files by timeframe
                timeframe_order = {'M1': 1, 'M5': 2, 'M15': 3, 'M30': 4, 'H1': 5, 'H4': 6, 'D1': 7, 'W1': 8, 'MN1': 9}
                files.sort(key=lambda x: timeframe_order.get(x[1]['timeframes'][0] if x[1]['timeframes'] else 'Unknown', 999))
                
                print(f"\n{Fore.GREEN}🔸 {symbol} ({source.upper()}) - {len(files)} files:")
                
                # Display files in compact format
                for filename, file_info in files:
                    timeframe = file_info['timeframes'][0] if file_info['timeframes'] else 'Unknown'
                    size_mb = file_info['size_mb']
                    rows = file_info['rows']
                    start_date = file_info['start_date'][:10] if file_info['start_date'] != "No time data" else "No data"
                    end_date = file_info['end_date'][:10] if file_info['end_date'] != "No time data" else "No data"
                    
                    print(f"  {Fore.WHITE}{timeframe:>4} │ {size_mb:>6.1f}MB │ {rows:>8,} rows │ {start_date} to {end_date}")
        
        # Ask user to choose symbol and source
        print(f"\n{Fore.GREEN}📊 Data Loading Configuration")
        print(f"{Fore.CYAN}{'─'*50}")
        
        # Get symbol from user with default
        # Extract first available symbol from sorted_symbols
        default_symbol = 'btcusdt'  # fallback default
        if sorted_symbols:
            # Get the first symbol from the first available source_symbol pair
            first_symbol_key = sorted_symbols[0]
            default_symbol = first_symbol_key.split('_', 1)[1]  # Extract symbol part
        
        symbol_input = input(f"{Fore.GREEN}Choose Symbol to load data into memory (e.g., 'btcusdt') [default: {default_symbol}]: {Style.RESET_ALL}").strip().upper()
        if not symbol_input:
            symbol_input = default_symbol
            print(f"{Fore.YELLOW}Using default symbol: {symbol_input}")
        
        # Check if symbol exists
        available_symbols = []
        for symbol_key in sorted_symbols:
            source, symbol = symbol_key.split('_', 1)
            if symbol == symbol_input:
                available_symbols.append((source, symbol))
        
        if not available_symbols:
            print(f"{Fore.RED}❌ Symbol '{symbol_input}' not found in available symbols.")
            print(f"{Fore.YELLOW}Available symbols: {', '.join(set(s.split('_', 1)[1] for s in sorted_symbols))}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # If multiple sources found, let user choose
        if len(available_symbols) > 1:
            print(f"\n{Fore.YELLOW}⚠️  Multiple sources found for {symbol_input}:")
            for i, (source, symbol) in enumerate(available_symbols, 1):
                print(f"  {i}. {source.upper()}")
            
            try:
                source_choice = input(f"\n{Fore.GREEN}Choose source (1-{len(available_symbols)}) [default: 1]: {Style.RESET_ALL}").strip()
                if not source_choice:
                    source_choice = "1"
                source_idx = int(source_choice) - 1
                if source_idx < 0 or source_idx >= len(available_symbols):
                    raise ValueError("Invalid choice")
                selected_source, selected_symbol = available_symbols[source_idx]
            except (ValueError, IndexError):
                print(f"{Fore.RED}❌ Invalid choice. Using first source.")
                selected_source, selected_symbol = available_symbols[0]
        else:
            selected_source, selected_symbol = available_symbols[0]
        
        print(f"\n{Fore.GREEN}✅ Selected: {selected_symbol} from {selected_source.upper()}")
        
        # Load and process data with MTF structure creation
        self._load_and_process_raw_parquet_data(selected_symbol, selected_source, analyzer, loader, processor, mtf_creator)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_and_process_raw_parquet_data(self, symbol: str, source: str, analyzer: 'RawParquetAnalyzer', loader: 'RawParquetLoader', processor: 'RawParquetProcessor', mtf_creator: 'RawParquetMTFCreator'):
        """Load and process raw parquet data with MTF structure creation."""
        print(f"\n{Fore.YELLOW}🔄 Loading and processing {symbol} data from {source}...")
        
        try:
            # Load data for the symbol from specific source
            print(f"{Fore.CYAN}📊 Loading data from {source}...")
            result = loader.load_symbol_data(symbol, source)
            
            if result["status"] != "success":
                print(f"{Fore.RED}❌ Error loading data: {result['message']}")
                return
            
            # Process the loaded data
            print(f"{Fore.CYAN}🔄 Processing data...")
            processed_result = processor.process_symbol_data(result)
            
            if processed_result["status"] != "success":
                print(f"{Fore.RED}❌ Error processing data: {processed_result['message']}")
                return
            
            # Show available timeframes
            available_timeframes = list(processed_result['data'].keys())
            print(f"{Fore.GREEN}📊 Available timeframes: {', '.join(available_timeframes)}")
            
            # Get main timeframe from user
            print(f"\n{Fore.YELLOW}Choose Main Time Frame for {symbol}:")
            print(f"{Fore.CYAN}{'─'*40}")
            for i, tf in enumerate(available_timeframes, 1):
                print(f"{Fore.WHITE}{i}. {tf}")
            print(f"{Fore.CYAN}{'─'*40}")
            
            try:
                choice_input = input(f"{Fore.GREEN}Enter choice (1-{len(available_timeframes)}) [default: 1]: {Style.RESET_ALL}").strip()
                if not choice_input:
                    choice_idx = 0
                else:
                    choice_idx = int(choice_input) - 1
                    
                if choice_idx < 0 or choice_idx >= len(available_timeframes):
                    raise ValueError("Invalid choice")
                main_timeframe = available_timeframes[choice_idx]
            except (ValueError, IndexError):
                print(f"{Fore.RED}❌ Invalid choice. Using first timeframe.")
                main_timeframe = available_timeframes[0]
            
            print(f"\n{Fore.GREEN}✅ Selected main timeframe: {main_timeframe}")
            
            # Create MTF structure
            print(f"\n{Fore.YELLOW}🔧 Creating MTF structure...")
            mtf_result = mtf_creator.create_mtf_from_processed_data(
                processed_result['data'], symbol, main_timeframe, source)
            
            if mtf_result["status"] == "success":
                print(f"\n{Fore.GREEN}✅ Successfully created MTF structure for {symbol}!")
                print(f"  • Source: {source}")
                print(f"  • Main timeframe: {main_timeframe}")
                print(f"  • Available timeframes: {', '.join(available_timeframes)}")
                print(f"  • Total rows: {processed_result['metadata']['total_rows']:,}")
                print(f"  • Size: {processed_result['metadata']['total_size_mb']:.1f} MB")
                
                # Save MTF structure to cleaned_data folder like in csv converted
                print(f"\n{Fore.YELLOW}💾 Saving MTF structure to cleaned_data folder...")
                self._save_raw_parquet_mtf_structure(symbol, mtf_result['mtf_data'], source)
                
                print(f"\n{Fore.GREEN}🎯 Ready for EDA, feature engineering, ML, backtesting, and monitoring!")
            else:
                print(f"\n{Fore.RED}❌ Error creating MTF structure: {mtf_result['message']}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error processing data: {e}")
            import traceback
            traceback.print_exc()
    
    def _save_raw_parquet_mtf_structure(self, symbol: str, mtf_data: Dict[str, Any], source: str):
        """Save raw parquet MTF structure to cleaned_data folder like csv converted."""
        try:
            from .data_loading import DataLoader
            import json
            
            # DataLoader will create the necessary directories
            
            # Use DataLoader to save MTF structure (same as csv converted)
            loader = DataLoader()
            
            # Create symbol info for DataLoader
            symbol_info = {
                'timeframes': mtf_data['timeframes'],
                'timeframe_details': {}
            }
            
            # Fill timeframe details
            for tf in mtf_data['timeframes']:
                df = mtf_data['timeframe_data'][tf]
                symbol_info['timeframe_details'][tf] = {
                    'size_mb': 0,  # Will be calculated by DataLoader
                    'rows': len(df),
                    'start_date': str(df.index.min()) if not df.empty else 'No data',
                    'end_date': str(df.index.max()) if not df.empty else 'No data',
                    'columns': list(df.columns)
                }
            
            # Save using DataLoader's method with data source
            loader._save_loaded_data(symbol, mtf_data['timeframe_data'], mtf_data, source)
            
            # Get the actual save directory from DataLoader
            source_dir = loader.mtf_dir / source
            symbol_mtf_dir = source_dir / symbol.lower()
            
            print(f"{Fore.GREEN}✅ MTF structure saved to: {symbol_mtf_dir}")
            print(f"  • Symbol: {symbol.upper()}")
            print(f"  • Source: {source}")
            print(f"  • Timeframes: {', '.join(mtf_data['timeframes'])}")
            print(f"  • Main timeframe: {mtf_data['main_timeframe']}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving MTF structure: {e}")
            import traceback
            traceback.print_exc()
    
    def _extract_source_and_symbol_from_filename(self, filename: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract source and symbol from filename."""
        try:
            # Remove extension
            name = filename.split('.')[0]
            
            # Look for patterns like source_SYMBOL_TIMEFRAME
            parts = name.split("_")
            if len(parts) >= 2:
                source = parts[0].lower()
                symbol = parts[1].upper()
                return source, symbol
            
            # Look for patterns like SYMBOL_source_TIMEFRAME
            if len(parts) >= 3:
                symbol = parts[0].upper()
                source = parts[1].lower()
                return source, symbol
            
            return None, None
        except Exception as e:
            print_error(f"Error extracting source and symbol from {filename}: {e}")
            return None, None
    
    def _load_indicators(self):
        """Load indicators data with detailed folder analysis and MTF structure creation."""
        print(f"\n{Fore.YELLOW}📈 Indicators Data Analysis...")
        
        # Show analysis progress
        analysis_start_time = time.time()
        
        # Create progress callback function
        def progress_callback(message: str, progress: float):
            self._show_indicators_progress(message, progress, analysis_start_time)
            # Small delay to make progress visible
            if progress < 1.0:
                time.sleep(0.05)
        
        # Import indicators modules
        from src.interactive.data_management.indicators import (
            IndicatorsAnalyzer, IndicatorsLoader, IndicatorsProcessor, IndicatorsMTFCreator
        )
        
        # Initialize components
        progress_callback("Initializing indicators modules", 0.0)
        analyzer = IndicatorsAnalyzer()
        loader = IndicatorsLoader()
        processor = IndicatorsProcessor()
        mtf_creator = IndicatorsMTFCreator()
        
        # Analyze folder with real-time progress updates
        analysis = analyzer.analyze_indicators_folder(progress_callback)
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "Indicators")
        
        # Display indicators found (only unique indicator names)
        if analysis["indicators"]:
            unique_indicators = list(set(analysis["indicators"]))
            unique_indicators.sort()
            print(f"\n{Fore.GREEN}📊 Available Indicators:")
            indicators_text = ", ".join(unique_indicators)
            print(f"{Fore.WHITE}  {indicators_text}")
        
        # Display subfolders information with detailed breakdown
        if analysis["subfolders_info"]:
            print(f"\n{Fore.YELLOW}📁 Subfolders Information:")
            for subdir, subfolder_info in analysis["subfolders_info"].items():
                print(f"\n{Fore.WHITE}🔸 {subdir.upper()}:")
                print(f"  • Files: {subfolder_info['file_count']}")
                print(f"  • Size: {subfolder_info['size_mb']} MB")
                print(f"  • Modified: {subfolder_info['modified']}")
        
        # Display files by source and indicator (like Raw Parquet)
        if analysis["files_info"]:
            self._display_indicators_by_source_and_indicator(analysis["files_info"])
        
        # Use interactive filtering system
        from src.interactive.data_management.data_filter import DataFilter
        
        data_filter = DataFilter()
        data_filter.set_available_data(analysis["files_info"])
        
        # Interactive filter selection
        format_filter, source_filter, symbol_filter, indicator_filter = data_filter.interactive_filter_selection(analysis["files_info"])
        
        # Apply filters
        filtered_files = data_filter.filter_files(
            analysis["files_info"],
            format_filter=format_filter,
            source_filter=source_filter,
            symbol_filter=symbol_filter,
            indicator_filter=indicator_filter
        )
        
        if not filtered_files:
            print(f"\n{Fore.RED}❌ No files match the selected filters")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display filtered results
        data_filter.display_filtered_results(filtered_files)
        
        # Show loading summary
        loading_summary = data_filter.get_loading_summary(filtered_files)
        print(f"\n{Fore.GREEN}📊 {loading_summary}")
        
        # Ask user what to do with the data
        print(f"\n{Fore.YELLOW}What would you like to do with the indicators data?")
        print(f"{Fore.WHITE}1. Save filtered indicators to MTF structure")
        print(f"{Fore.WHITE}0. Cancel")
        
        choice = input(f"\n{Fore.GREEN}Enter your choice (1/0): {Style.RESET_ALL}").strip()
        
        if choice == "0":
            print(f"{Fore.YELLOW}Operation cancelled.")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        elif choice == "1":
            # Save filtered indicators to MTF structure
            self._save_all_indicators_to_mtf(filtered_files, analyzer, loader, processor, mtf_creator)
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        else:
            print(f"{Fore.RED}Invalid choice. Operation cancelled.")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
    
    def _extract_timeframe_from_filename(self, filename: str) -> str:
        """Extract timeframe from filename."""
        try:
            # Remove extension
            name = filename.split('.')[0]
            
            # Common timeframe patterns
            timeframes = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN1']
            
            for tf in timeframes:
                if f'_{tf}_' in name or f'_{tf}.' in name or name.endswith(f'_{tf}'):
                    return tf
            
            # Special case for CSVExport files
            if 'CSVExport' in filename:
                # CSVExport_GOOG.NAS_PERIOD_MN1_Wave -> MN1
                # Look for PERIOD_ pattern in the full filename
                if 'PERIOD_' in filename:
                    period_part = filename.split('PERIOD_')[-1].split('.')[0]
                    if period_part in timeframes:
                        return period_part
                # Also check if any timeframe is in the filename
                for tf in timeframes:
                    if f'_{tf}_' in filename or f'_{tf}.' in filename or filename.endswith(f'_{tf}'):
                        return tf
            
            return 'Unknown'
            
        except Exception as e:
            return 'Unknown'
    
    def _display_indicators_by_source_and_indicator(self, files_info: Dict[str, Any]):
        """Display indicators grouped by source and indicator like Raw Parquet."""
        try:
            # Group files by source and indicator
            files_by_source_indicator = {}
            for filename, file_info in files_info.items():
                source = file_info.get('source', 'unknown')
                indicator = file_info.get('indicator', 'unknown')
                format_type = file_info.get('format', '').replace('.', '').upper()
                
                key = f"{source}_{indicator}_{format_type}"
                if key not in files_by_source_indicator:
                    files_by_source_indicator[key] = {
                        'source': source,
                        'indicator': indicator,
                        'format': format_type,
                        'files': []
                    }
                files_by_source_indicator[key]['files'].append((filename, file_info))
            
            # Sort by source, then indicator, then format
            sorted_keys = sorted(files_by_source_indicator.keys(), 
                               key=lambda x: (files_by_source_indicator[x]['source'], 
                                            files_by_source_indicator[x]['indicator'],
                                            files_by_source_indicator[x]['format']))
            
            print(f"\n{Fore.YELLOW}📋 Files by Source and Indicator ({len(sorted_keys)} groups):")
            print(f"{Fore.CYAN}{'─'*80}")
            
            for key in sorted_keys:
                group_info = files_by_source_indicator[key]
                source = group_info['source'].upper()
                indicator = group_info['indicator']
                format_type = group_info['format']
                files = group_info['files']
                
                # Calculate total size and rows
                total_size = sum(f[1]['size_mb'] for f in files)
                total_rows = sum(f[1]['rows'] for f in files)
                
                print(f"\n{Fore.GREEN}🔸 {indicator} ({source}) - {format_type} - {len(files)} files:")
                print(f"  {Fore.WHITE}Total: {total_size:.1f}MB, {total_rows:,} rows")
                
                # Sort files by symbol, then by timeframe
                def sort_key(file_tuple):
                    filename, file_info = file_tuple
                    symbol = self._extract_symbol_from_filename(filename)
                    timeframe = self._extract_timeframe_from_filename(filename)
                    # Sort by symbol first, then by timeframe
                    return (symbol or 'Unknown', timeframe)
                
                sorted_files = sorted(files, key=sort_key)
                
                # Group files by symbol for better display
                files_by_symbol = {}
                for filename, file_info in sorted_files:
                    symbol = self._extract_symbol_from_filename(filename)
                    if symbol not in files_by_symbol:
                        files_by_symbol[symbol] = []
                    files_by_symbol[symbol].append((filename, file_info))
                
                # Display files grouped by symbol
                for symbol, symbol_files in files_by_symbol.items():
                    if symbol:
                        print(f"    {Fore.CYAN}📊 {symbol}:")
                    
                    # Sort symbol files by timeframe
                    symbol_files.sort(key=lambda x: self._extract_timeframe_from_filename(x[0]))
                    
                    for filename, file_info in symbol_files:
                        timeframe = self._extract_timeframe_from_filename(filename)
                        size_mb = file_info['size_mb']
                        rows = file_info['rows']
                        start_date = file_info['start_date'][:10] if file_info['start_date'] != "No time data" else "No data"
                        end_date = file_info['end_date'][:10] if file_info['end_date'] != "No time data" else "No data"
                        
                        # Format: " M1 │  121.8MB │ 3,704,799 rows │ 2017-08-31 to 2025-09-16"
                        print(f"      {Fore.WHITE} {timeframe:<3} │ {size_mb:>7.1f}MB │ {rows:>8,} rows │ {start_date} to {end_date}")
            
            print(f"{Fore.CYAN}{'─'*80}")
            
        except Exception as e:
            print_error(f"Error displaying indicators by source: {e}")
    
    def _get_available_combinations(self, files_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get available combinations of source, format, and indicator."""
        try:
            combinations = {}
            
            for filename, file_info in files_info.items():
                source = file_info.get('source', 'unknown')
                indicator = file_info.get('indicator', 'unknown')
                format_type = file_info.get('format', '').replace('.', '').lower()
                
                key = f"{source}_{indicator}_{format_type}"
                
                if key not in combinations:
                    combinations[key] = {
                        'source': source,
                        'indicator': indicator,
                        'format': format_type,
                        'file_count': 0,
                        'total_size': 0,
                        'total_rows': 0,
                        'files': []
                    }
                
                combinations[key]['file_count'] += 1
                combinations[key]['total_size'] += file_info.get('size_mb', 0)
                combinations[key]['total_rows'] += file_info.get('rows', 0)
                combinations[key]['files'].append((filename, file_info))
            
            # Convert to list and sort
            result = list(combinations.values())
            result.sort(key=lambda x: (x['source'], x['indicator'], x['format']))
            
            return result
            
        except Exception as e:
            print_error(f"Error getting available combinations: {e}")
            return []
    
    def _load_and_process_filtered_indicators_data(self, filtered_files: List[Dict[str, Any]], format_name: str, 
                                                 analyzer: 'IndicatorsAnalyzer', loader: 'IndicatorsLoader', 
                                                 processor: 'IndicatorsProcessor', mtf_creator: 'IndicatorsMTFCreator'):
        """Load and process only filtered indicators data with MTF structure creation."""
        print(f"\n{Fore.YELLOW}🔄 Loading and processing filtered indicators data from {format_name}...")
        
        start_time = time.time()
        
        try:
            # Load only the filtered files
            loaded_data = {}
            total_files = len(filtered_files)
            
            for i, file_info in enumerate(filtered_files):
                # Calculate progress for loading files (0-40%)
                progress = (i + 1) / total_files * 0.4
                self._show_unified_progress(f"Loading {file_info['filename']}", progress, start_time)
                
                # Load specific file by filename
                result = loader.load_specific_file(file_info['filename'])
                
                if result["status"] == "success":
                    loaded_data[file_info['filename']] = result['data']
                else:
                    print(f"\n{Fore.RED}❌ Failed to load {file_info['filename']}: {result.get('message', 'Unknown error')}")
            
            if not loaded_data:
                print(f"\n{Fore.RED}❌ No filtered indicators data loaded successfully")
                return
            
            # Process the loaded data (40-60%)
            self._show_unified_progress("Processing indicators data", 0.4, start_time)
            processed_result = processor.process_indicators_data(loaded_data, show_detailed_progress=False)
            
            if processed_result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error processing data: {processed_result['message']}")
                return
            
            self._show_unified_progress("Processing indicators data", 0.6, start_time)
            
            # Get symbol from filtered files (should be the same for all)
            symbol_input = filtered_files[0]['symbol'].upper()
            
            # Create MTF structure (60-90%)
            self._show_unified_progress("Creating MTF structure", 0.6, start_time)
            # Use default timeframe for now, will be updated later
            timeframe_input = "M1"
            mtf_result = mtf_creator.create_mtf_from_processed_data(
                processed_result['data'], symbol_input, timeframe_input, 'indicators')
            
            if mtf_result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error creating MTF structure: {mtf_result['message']}")
                return
            
            self._show_unified_progress("Creating MTF structure", 0.9, start_time)
            
            # Save MTF structure to cleaned_data folder (90-100%)
            self._show_unified_progress("Saving MTF structure", 0.9, start_time)
            self._save_indicators_mtf_structure(symbol_input, "filtered_indicators", mtf_result['mtf_data'], format_name)
            
            # Complete progress
            self._show_unified_progress("Saving MTF structure", 1.0, start_time)
            
            # Get main timeframe from user after progress is complete
            print(f"\n{Fore.GREEN}Using symbol from filtered data: {symbol_input}")
            timeframe_input = input(f"{Fore.GREEN}Enter main timeframe (e.g., 'M1', 'H1', 'D1') [default: M1]: {Style.RESET_ALL}").strip().upper()
            if not timeframe_input:
                timeframe_input = "M1"
                print(f"{Fore.YELLOW}Using default timeframe: {timeframe_input}")
            
            # Show success message
            print(f"\n{Fore.GREEN}✅ Successfully created MTF structure for filtered indicators!")
            print(f"  • Symbol: {symbol_input}")
            print(f"  • Format: {format_name}")
            print(f"  • Main Timeframe: {timeframe_input}")
            print(f"  • Total rows: {processed_result['metadata']['total_rows']:,}")
            print(f"  • Files processed: {len(loaded_data)}")
            print(f"  • Creation time: {mtf_result['creation_time']:.2f} seconds")
            print(f"\n{Fore.GREEN}🎯 Ready for EDA, feature engineering, ML, backtesting, and monitoring!")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error processing filtered indicators data: {e}")
            import traceback
            traceback.print_exc()
    
    def _load_and_process_all_indicators_data(self, format_name: str, analyzer: 'IndicatorsAnalyzer', 
                                            loader: 'IndicatorsLoader', processor: 'IndicatorsProcessor', 
                                            mtf_creator: 'IndicatorsMTFCreator'):
        """Load and process all indicators data with MTF structure creation."""
        print(f"\n{Fore.YELLOW}🔄 Loading and processing all indicators data from {format_name}...")
        
        # Define processing steps
        steps = [
            "Loading all indicators data",
            "Processing all indicators data", 
            "Creating MTF structure",
            "Saving MTF structure"
        ]
        total_steps = len(steps)
        start_time = time.time()
        
        try:
            # Step 1: Load all data for the specific format
            self._show_indicators_progress("Loading all indicators data", 0.0, start_time, "1", total_steps)
            result = loader.load_indicators_by_format(format_name)
            
            if result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error loading data: {result['message']}")
                return
            
            # Update progress
            self._show_indicators_progress("Loading all indicators data", 0.25, start_time, "1", total_steps)
            
            # Step 2: Process all the loaded data
            self._show_indicators_progress("Processing all indicators data", 0.25, start_time, "2", total_steps)
            processed_result = processor.process_indicators_data(result['data'], show_detailed_progress=False)
            
            if processed_result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error processing data: {processed_result['message']}")
                return
            
            # Update progress
            self._show_indicators_progress("Processing all indicators data", 0.5, start_time, "2", total_steps)
            
            # Get symbol from user
            symbol_input = input(f"\n{Fore.GREEN}Enter symbol for MTF structure (e.g., 'BTCUSDT') [default: BTCUSDT]: {Style.RESET_ALL}").strip().upper()
            if not symbol_input:
                symbol_input = "BTCUSDT"
                print(f"{Fore.YELLOW}Using default symbol: {symbol_input}")
            
            # Get main timeframe from user
            timeframe_input = input(f"{Fore.GREEN}Enter main timeframe (e.g., 'M1', 'H1', 'D1') [default: M1]: {Style.RESET_ALL}").strip().upper()
            if not timeframe_input:
                timeframe_input = "M1"
                print(f"{Fore.YELLOW}Using default timeframe: {timeframe_input}")
            
            # Step 3: Create MTF structure
            self._show_indicators_progress("Creating MTF structure", 0.5, start_time, "3", total_steps)
            mtf_result = mtf_creator.create_mtf_from_processed_data(
                processed_result['data'], symbol_input, timeframe_input, 'indicators')
            
            if mtf_result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error creating MTF structure: {mtf_result['message']}")
                return
            
            # Update progress
            self._show_indicators_progress("Creating MTF structure", 0.75, start_time, "3", total_steps)
            
            # Step 4: Save MTF structure to cleaned_data folder
            self._show_indicators_progress("Saving MTF structure", 0.75, start_time, "4", total_steps)
            self._save_indicators_mtf_structure(symbol_input, "all_indicators", mtf_result['mtf_data'], format_name)
            
            # Complete progress
            self._show_indicators_progress("Saving MTF structure", 1.0, start_time, "4", total_steps)
            
            # Show success message
            print(f"\n{Fore.GREEN}✅ Successfully created MTF structure for all indicators!")
            print(f"  • Symbol: {symbol_input}")
            print(f"  • Format: {format_name}")
            print(f"  • Main Timeframe: {timeframe_input}")
            print(f"  • Total rows: {processed_result['metadata']['total_rows']:,}")
            print(f"  • Creation time: {mtf_result['creation_time']:.2f} seconds")
            print(f"\n{Fore.GREEN}🎯 Ready for EDA, feature engineering, ML, backtesting, and monitoring!")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error processing all indicators data: {e}")
            import traceback
            traceback.print_exc()
    
    def _load_and_process_indicators_data(self, indicator: str, format_name: str, analyzer: 'IndicatorsAnalyzer', 
                                        loader: 'IndicatorsLoader', processor: 'IndicatorsProcessor', 
                                        mtf_creator: 'IndicatorsMTFCreator'):
        """Load and process indicators data with MTF structure creation."""
        print(f"\n{Fore.YELLOW}🔄 Loading and processing {indicator} data from {format_name}...")
        
        # Define processing steps
        steps = [
            "Loading data",
            "Processing data", 
            "Creating MTF structure",
            "Saving MTF structure"
        ]
        total_steps = len(steps)
        start_time = time.time()
        
        try:
            # Step 1: Load data for the specific indicator and format
            self._show_indicators_progress("Loading indicator data", 0.0, start_time, "1", total_steps)
            result = loader.load_indicator_by_name(indicator, format_name)
            
            if result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error loading data: {result['message']}")
                return
            
            # Update progress
            self._show_indicators_progress("Loading indicator data", 0.25, start_time, "1", total_steps)
            
            # Step 2: Process the loaded data
            self._show_indicators_progress("Processing indicator data", 0.25, start_time, "2", total_steps)
            processed_result = processor.process_single_indicator(result['data'])
            
            if processed_result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error processing data: {processed_result['message']}")
                return
            
            # Update progress
            self._show_indicators_progress("Processing indicator data", 0.5, start_time, "2", total_steps)
            
            # Get symbol from user
            symbol_input = input(f"\n{Fore.GREEN}Enter symbol for MTF structure (e.g., 'BTCUSDT') [default: BTCUSDT]: {Style.RESET_ALL}").strip().upper()
            if not symbol_input:
                symbol_input = "BTCUSDT"
                print(f"{Fore.YELLOW}Using default symbol: {symbol_input}")
            
            # Get timeframe from user
            timeframe_input = input(f"{Fore.GREEN}Enter timeframe (e.g., 'M1', 'H1', 'D1') [default: M1]: {Style.RESET_ALL}").strip().upper()
            if not timeframe_input:
                timeframe_input = "M1"
                print(f"{Fore.YELLOW}Using default timeframe: {timeframe_input}")
            
            # Step 3: Create MTF structure
            self._show_indicators_progress("Creating MTF structure", 0.5, start_time, "3", total_steps)
            mtf_result = mtf_creator.create_mtf_from_single_indicator(
                processed_result['data'], symbol_input, timeframe_input)
            
            if mtf_result["status"] != "success":
                print(f"\n{Fore.RED}❌ Error creating MTF structure: {mtf_result['message']}")
                return
            
            # Update progress
            self._show_indicators_progress("Creating MTF structure", 0.75, start_time, "3", total_steps)
            
            # Step 4: Save MTF structure to cleaned_data folder
            self._show_indicators_progress("Saving MTF structure", 0.75, start_time, "4", total_steps)
            self._save_indicators_mtf_structure(symbol_input, indicator, mtf_result['mtf_data'], format_name)
            
            # Complete progress
            self._show_indicators_progress("Saving MTF structure", 1.0, start_time, "4", total_steps)
            
            # Show success message
            print(f"\n{Fore.GREEN}✅ Successfully created MTF structure for {indicator}!")
            print(f"  • Symbol: {symbol_input}")
            print(f"  • Indicator: {indicator}")
            print(f"  • Format: {format_name}")
            print(f"  • Timeframe: {timeframe_input}")
            print(f"  • Total rows: {processed_result['data']['rows']:,}")
            print(f"  • Creation time: {mtf_result['creation_time']:.2f} seconds")
            print(f"\n{Fore.GREEN}🎯 Ready for EDA, feature engineering, ML, backtesting, and monitoring!")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error processing indicators data: {e}")
            import traceback
            traceback.print_exc()
    
    def _save_indicators_mtf_structure(self, symbol: str, indicator: str, mtf_data: Dict[str, Any], source: str):
        """Save indicators MTF structure to cleaned_data folder."""
        try:
            from .data_loading import DataLoader
            import json
            
            # Use DataLoader to save MTF structure (same as other data sources)
            loader = DataLoader()
            
            # Convert indicator_data to the format expected by DataLoader
            # DataLoader expects {timeframe: DataFrame} format
            timeframe_data = {}
            
            # Extract data from indicator_data structure
            if 'indicator_data' in mtf_data:
                for indicator_name, timeframes_data in mtf_data['indicator_data'].items():
                    for timeframe, file_data in timeframes_data.items():
                        if isinstance(file_data, dict) and 'data' in file_data:
                            df = file_data['data']
                            if not df.empty:
                                # Use timeframe as key for DataLoader
                                timeframe_data[timeframe] = df
            
            # If no timeframe_data found, try to use main_data
            if not timeframe_data and 'main_data' in mtf_data:
                main_data = mtf_data['main_data']
                if not main_data.empty:
                    # Use main_timeframe as key
                    main_tf = mtf_data.get('main_timeframe', 'M1')
                    timeframe_data[main_tf] = main_data
            
            # Convert cross_timeframe_features to the format expected by DataLoader
            # DataLoader expects {timeframe: DataFrame} but we have {timeframe: {indicator: DataFrame}}
            cross_timeframe_features = {}
            if 'cross_timeframe_features' in mtf_data:
                for timeframe, indicators_data in mtf_data['cross_timeframe_features'].items():
                    # Combine all indicators for this timeframe into one DataFrame
                    combined_dfs = []
                    for indicator, df in indicators_data.items():
                        if not df.empty:
                            # Add indicator prefix to column names to avoid conflicts
                            df_copy = df.copy()
                            df_copy.columns = [f"{indicator}_{col}" for col in df_copy.columns]
                            combined_dfs.append(df_copy)
                    
                    if combined_dfs:
                        # Combine all DataFrames for this timeframe
                        import pandas as pd
                        combined_df = pd.concat(combined_dfs, axis=1, sort=True)
                        cross_timeframe_features[timeframe] = combined_df
            
            # Update mtf_data with converted cross_timeframe_features
            if cross_timeframe_features:
                mtf_data['cross_timeframe_features'] = cross_timeframe_features
            
            # Only save if we have data
            if timeframe_data:
                # Save using DataLoader's method with data source
                loader._save_loaded_data(symbol, timeframe_data, mtf_data, f"{source}_{indicator}")
            else:
                print(f"{Fore.YELLOW}⚠️ No valid data found to save for {symbol} {indicator}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving MTF structure: {e}")
            import traceback
            traceback.print_exc()
    
    def _load_cleaned_data(self):
        """Load pre-created MTF structures for fast ML analysis."""
        print(f"\n{Fore.YELLOW}✨ MTF Data Structures Analysis...")
        
        try:
            from .data_loading import SymbolAnalyzer, DataLoader, SymbolDisplay
            from pathlib import Path
            import json
            
            # Initialize components
            symbol_analyzer = SymbolAnalyzer()
            data_loader = DataLoader()
            symbol_display = SymbolDisplay()
            
            # Check for existing MTF structures in new source-based structure
            mtf_dir = Path("data/cleaned_data/mtf_structures")
            
            if not mtf_dir.exists():
                print(f"{Fore.RED}❌ No MTF structures found")
                print(f"{Fore.YELLOW}💡 Please first create MTF structures using 'Load Data -> CSV Converted'")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Get all source directories
            source_dirs = [f for f in mtf_dir.iterdir() if f.is_dir()]
            
            if not source_dirs:
                print(f"{Fore.RED}❌ No MTF source directories found")
                print(f"{Fore.YELLOW}💡 Please first create MTF structures using 'Load Data -> CSV Converted'")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Get all symbol MTF folders from all source directories
            mtf_symbol_folders = []
            for source_dir in source_dirs:
                # Handle special case for gaps_fixed which has nested structure: gaps_fixed/source/symbol/
                if source_dir.name == 'gaps_fixed':
                    # For gaps_fixed, we need to go one level deeper
                    for nested_source_dir in source_dir.iterdir():
                        if nested_source_dir.is_dir():
                            symbol_folders = [f for f in nested_source_dir.iterdir() if f.is_dir()]
                            for symbol_folder in symbol_folders:
                                # Store source information with original source name
                                folder_info = {
                                    'path': symbol_folder,
                                    'source': nested_source_dir.name  # Use the actual source (e.g., 'binance')
                                }
                                mtf_symbol_folders.append(folder_info)
                else:
                    # Normal two-level structure: source/symbol/
                    symbol_folders = [f for f in source_dir.iterdir() if f.is_dir()]
                    for symbol_folder in symbol_folders:
                        # Store source information in a dictionary
                        folder_info = {
                            'path': symbol_folder,
                            'source': source_dir.name
                        }
                        mtf_symbol_folders.append(folder_info)
            
            if not mtf_symbol_folders:
                print(f"{Fore.RED}❌ No MTF symbol folders found")
                print(f"{Fore.YELLOW}💡 Please first create MTF structures using 'Load Data -> CSV Converted'")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Analyze MTF structures
            mtf_info = {}
            total_size = 0
            
            for folder_info in sorted(mtf_symbol_folders, key=lambda x: (x['source'], x['path'].name)):
                symbol_folder = folder_info['path']
                symbol_name = symbol_folder.name.upper()
                source_name = folder_info['source']
                mtf_metadata_file = symbol_folder / "mtf_metadata.json"
                
                if mtf_metadata_file.exists():
                    try:
                        with open(mtf_metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        # Calculate folder size
                        folder_size = sum(f.stat().st_size for f in symbol_folder.rglob('*') if f.is_file())
                        folder_size_mb = folder_size / (1024 * 1024)
                        total_size += folder_size_mb
                        
                        # Create unique key that includes source and path to avoid conflicts
                        # For gaps_fixed data, include the full path to make it unique
                        if 'gaps_fixed' in str(symbol_folder):
                            symbol_key = f"{symbol_name}_{source_name}_gaps_fixed"
                        else:
                            symbol_key = f"{symbol_name}_{source_name}"
                        
                        # Determine folder name for display
                        folder_name = 'original'
                        if 'gaps_fixed' in str(symbol_folder):
                            folder_name = 'gaps_fixed'
                        
                        mtf_info[symbol_key] = {
                            'symbol': metadata.get('symbol', symbol_name),
                            'source': source_name,
                            'folder_name': folder_name,
                            'main_timeframe': metadata.get('main_timeframe', 'M1'),
                            'timeframes': metadata.get('timeframes', []),
                            'total_rows': metadata.get('total_rows', 0),
                            'main_data_shape': metadata.get('main_data_shape', [0, 0]),
                            'cross_timeframes': metadata.get('cross_timeframes', []),
                            'created_at': metadata.get('created_at', 'Unknown'),
                            'size_mb': folder_size_mb,
                            'file_count': len(list(symbol_folder.glob('*.parquet'))),
                            'folder_path': str(symbol_folder)
                        }
                    except Exception as e:
                        print_error(f"Error reading MTF metadata for {symbol_name}: {e}")
                        continue
            
            if not mtf_info:
                print(f"{Fore.RED}❌ No valid MTF structures found")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Display MTF structures table
            print(f"\n{Fore.GREEN}🎯 Available MTF Structures ({len(mtf_info)}):")
            print(f"{Fore.CYAN}{'─'*120}")
            print(f"{Fore.WHITE}{'Symbol':<12} {'Folder':<12} {'Source':<10} {'Size (MB)':<10} {'Files':<6} {'Main TF':<8} {'Timeframes':<20} {'Rows':<12} {'Created':<12}")
            print(f"{Fore.CYAN}{'─'*120}")
            
            for symbol_key, info in mtf_info.items():
                timeframes_str = ', '.join(info['timeframes'][:3])
                if len(info['timeframes']) > 3:
                    timeframes_str += f" +{len(info['timeframes'])-3} more"
                
                created_date = info['created_at'][:10] if info['created_at'] != 'Unknown' else 'Unknown'
                
                print(f"{Fore.WHITE}{info['symbol']:<12} {info['folder_name']:<12} {info['source']:<10} {info['size_mb']:<10.1f} {info['file_count']:<6} {info['main_timeframe']:<8} {timeframes_str:<20} {info['total_rows']:<12,} {created_date:<12}")
            
            print(f"{Fore.CYAN}{'─'*120}")
            print(f"{Fore.YELLOW}Total: {len(mtf_info)} MTF structures, {total_size:.1f} MB")
            
            # Get symbol choice from user - show only symbol names without source
            available_symbols = [info['symbol'] for info in mtf_info.values()]
            symbol_choice = symbol_display.get_symbol_choice(available_symbols)
            
            if not symbol_choice:
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Find the selected symbol info (handle multiple sources for same symbol)
            matching_symbols = []
            for symbol_key, info in mtf_info.items():
                if info['symbol'] == symbol_choice.upper():
                    matching_symbols.append(info)
            
            if not matching_symbols:
                print(f"{Fore.RED}❌ Symbol '{symbol_choice.upper()}' not found")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # If multiple sources found, let user choose
            if len(matching_symbols) > 1:
                print(f"\n{Fore.YELLOW}⚠️  Multiple sources found for {symbol_choice.upper()}:")
                for i, info in enumerate(matching_symbols, 1):
                    print(f"  {i}. {info['source']} - {info['size_mb']:.1f} MB, {info['total_rows']:,} rows")
                
                try:
                    source_choice = input(f"\n{Fore.GREEN}Choose source (1-{len(matching_symbols)}) [default: 1]: {Style.RESET_ALL}").strip()
                    if not source_choice:
                        source_choice = "1"
                    source_idx = int(source_choice) - 1
                    if source_idx < 0 or source_idx >= len(matching_symbols):
                        raise ValueError("Invalid choice")
                    selected_mtf_info = matching_symbols[source_idx]
                except (ValueError, IndexError):
                    print(f"{Fore.RED}❌ Invalid choice. Using first source.")
                    selected_mtf_info = matching_symbols[0]
            else:
                selected_mtf_info = matching_symbols[0]
            
            # Display MTF structure info
            print(f"\n{Fore.GREEN}🎯 {selected_mtf_info['symbol']} ({selected_mtf_info['source']}) - MTF Structure Info:")
            print(f"{Fore.CYAN}{'─'*60}")
            print(f"  • Source: {selected_mtf_info['source']}")
            print(f"  • Main Timeframe: {selected_mtf_info['main_timeframe']}")
            print(f"  • Available Timeframes: {', '.join(selected_mtf_info['timeframes'])}")
            print(f"  • Total Rows: {selected_mtf_info['total_rows']:,}")
            print(f"  • Main Data Shape: {selected_mtf_info['main_data_shape']}")
            print(f"  • Cross-timeframes: {len(selected_mtf_info['cross_timeframes'])}")
            print(f"  • Created: {selected_mtf_info['created_at']}")
            print(f"  • Size: {selected_mtf_info['size_mb']:.1f} MB")
            print(f"{Fore.CYAN}{'─'*60}")
            
            # Load MTF structure
            print(f"\n{Fore.YELLOW}🔄 Loading MTF structure into memory...")
            result = self._load_mtf_structure(selected_mtf_info['symbol'], selected_mtf_info)
            
            if result['status'] == 'success':
                # Save loaded data to global state
                from src.interactive.data_state_manager import data_state_manager
                
                # Prepare metadata for state manager
                loaded_metadata = {
                    'symbol': selected_mtf_info['symbol'],
                    'source': selected_mtf_info['source'],
                    'main_timeframe': selected_mtf_info['main_timeframe'],
                    'timeframes': selected_mtf_info['timeframes'],
                    'total_rows': selected_mtf_info['total_rows'],
                    'main_data_shape': selected_mtf_info['main_data_shape'],
                    'cross_timeframes': selected_mtf_info['cross_timeframes'],
                    'created_at': selected_mtf_info['created_at'],
                    'size_mb': selected_mtf_info['size_mb'],
                    'data_path': selected_mtf_info['folder_path'],  # Add the actual path
                    'data_type': 'mtf_structure'  # Mark as MTF structure
                }
                
                # Set loaded data in global state
                data_state_manager.set_loaded_data(result, loaded_metadata, result['memory_used'])
                
                print(f"\n{Fore.GREEN}✅ MTF structure loaded successfully!")
                print(f"  • Symbol: {selected_mtf_info['symbol']}")
                print(f"  • Source: {selected_mtf_info['source']}")
                print(f"  • Main data shape: {result['main_data'].shape}")
                print(f"  • Cross-timeframes: {len(result['cross_timeframes'])}")
                print(f"  • Memory used: {result['memory_used']:.1f} MB")
                print(f"  • Loading time: {result['loading_time']:.2f} seconds")
                print(f"\n{Fore.GREEN}🎯 Ready for EDA, feature engineering, ML, backtesting, and monitoring!")
            else:
                print(f"\n{Fore.RED}❌ Error loading MTF structure: {result['message']}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error in MTF data loading: {e}")
            import traceback
            traceback.print_exc()
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_mtf_structure(self, symbol: str, mtf_info: Dict[str, Any]) -> Dict[str, Any]:
        """Load MTF structure from saved files."""
        try:
            import psutil
            import time
            import pandas as pd
            from pathlib import Path
            
            # Get initial memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
            
            start_time = time.time()
            
            # Load main data using the correct path with source
            source = mtf_info.get('source', 'unknown')
            folder_name = mtf_info.get('folder_name', 'original')
            
            # Build correct path based on folder type
            if folder_name == 'gaps_fixed':
                mtf_dir = Path("data/cleaned_data/mtf_structures") / "gaps_fixed" / source / symbol.lower()
            else:
                mtf_dir = Path("data/cleaned_data/mtf_structures") / source / symbol.lower()
            
            main_file = mtf_dir / f"{symbol.lower()}_main_{mtf_info['main_timeframe'].lower()}.parquet"
            
            if not main_file.exists():
                return {'status': 'error', 'message': f'Main data file not found: {main_file}'}
            
            main_data = pd.read_parquet(main_file)
            
            # Load cross-timeframe features
            cross_timeframes = {}
            cross_dir = mtf_dir / "cross_timeframes"
            
            if cross_dir.exists():
                for tf in mtf_info['cross_timeframes']:
                    cross_file = cross_dir / f"{symbol.lower()}_{tf.lower()}_cross.parquet"
                    if cross_file.exists():
                        cross_timeframes[tf] = pd.read_parquet(cross_file)
            
            # Get final memory usage
            final_memory = process.memory_info().rss / (1024 * 1024)  # MB
            memory_used = final_memory - initial_memory
            loading_time = time.time() - start_time
            
            return {
                'status': 'success',
                'main_data': main_data,
                'cross_timeframes': cross_timeframes,
                'memory_used': memory_used,
                'loading_time': loading_time,
                'metadata': mtf_info
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
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
            import re
            
            # Common patterns for symbol extraction - more specific patterns
            patterns = [
                r'^([A-Z]{3,6}USD[A-Z]?)',  # BTCUSDT, EURUSD, etc. at start
                r'^([A-Z]{3,6}_[A-Z]{3,6})',  # BTC_USDT, EUR_USD, etc. at start
                r'([A-Z]{3,6}USD[A-Z]?)_',  # BTCUSDT_, EURUSD_ in middle
                r'([A-Z]{3,6}_[A-Z]{3,6})_',  # BTC_USDT_, EUR_USD_ in middle
                r'^([A-Z]{3,6})_',  # AAPL_, BTC_, etc. at start
            ]
            
            for pattern in patterns:
                match = re.search(pattern, filename.upper())
                if match:
                    symbol = match.group(1).replace('_', '')
                    # Validate that the symbol looks like a trading pair
                    if len(symbol) >= 3 and symbol.isalpha():
                        return symbol
            
            # Fallback to original logic for other patterns
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
    
    def _save_all_indicators_to_mtf(self, filtered_files: List[Dict[str, Any]], 
                                   analyzer: 'IndicatorsAnalyzer', loader: 'IndicatorsLoader', 
                                   processor: 'IndicatorsProcessor', mtf_creator: 'IndicatorsMTFCreator'):
        """Save filtered indicators to MTF structure like Raw Parquet functionality."""
        print(f"\n{Fore.YELLOW}🔧 Saving filtered indicators to MTF structure...")
        
        try:
            # Get format from first file
            if not filtered_files:
                print(f"\n{Fore.RED}❌ No files to process")
                return
            
            format_name = filtered_files[0]['format']
            
            # Use the new method that loads only filtered indicators
            self._load_and_process_filtered_indicators_data(filtered_files, format_name, analyzer, loader, processor, mtf_creator)
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error saving filtered indicators to MTF: {e}")
            import traceback
            traceback.print_exc()
