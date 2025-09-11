# -*- coding: utf-8 -*-
"""
Data Loader for NeoZork Interactive ML Trading Strategy Development.

This module provides utilities for loading symbol data with modern progress
tracking, memory monitoring, and MTF structure creation.
"""

import time
import pickle
import json
import psutil
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from colorama import Fore, Style
from src.common.logger import print_error


class DataLoader:
    """
    Data loader with modern progress tracking and memory monitoring.
    
    Features:
    - Load all timeframes for a symbol
    - Modern progress bar with ETA
    - Memory usage monitoring
    - MTF structure creation
    - Data caching and persistence
    """
    
    def __init__(self):
        """Initialize the data loader."""
        self.data_root = Path("data/cleaned_data")
        self.mtf_dir = self.data_root / "mtf_structures"
        self.mtf_dir.mkdir(parents=True, exist_ok=True)
    
    def load_symbol_data_with_progress(self, symbol: str, symbol_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load symbol data with modern progress tracking and memory usage display.
        
        Args:
            symbol: Symbol name (e.g., 'EURUSD')
            symbol_info: Symbol analysis information
            
        Returns:
            Dictionary with loaded data and metadata
        """
        print(f"\n{Fore.YELLOW}🔄 Loading {symbol.upper()} data into memory...")
        
        try:
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
            self._show_loading_progress(f"Completed loading {total_timeframes} timeframes", 
                                      1.0, "", f"{total_timeframes / total_time:.1f} tf/s")
            
            # Get final memory usage
            final_memory = process.memory_info().rss / (1024 * 1024)  # MB
            memory_used = final_memory - initial_memory
            
            # Display loading results
            self._display_loading_results(symbol, loaded_data, symbol_info, 
                                        total_time, memory_used, final_memory)
            
            # Create MTF (Multi-Timeframe) data structure for ML
            print(f"\n{Fore.YELLOW}🔧 Creating MTF data structure for ML...")
            mtf_data = self._create_mtf_structure(loaded_data, symbol)
            
            # Save loaded data for future use
            self._save_loaded_data(symbol, loaded_data, mtf_data)
            
            print(f"\n{Fore.GREEN}🎯 MTF data structure created and saved!")
            print(f"  • Symbol: {symbol.upper()}")
            print(f"  • Available timeframes: {', '.join(loaded_data.keys())}")
            print(f"  • Data shape: {mtf_data['main_data'].shape if 'main_data' in mtf_data else 'N/A'}")
            
            return {
                'status': 'success',
                'symbol': symbol.upper(),
                'loaded_data': loaded_data,
                'mtf_data': mtf_data,
                'memory_used': memory_used,
                'loading_time': total_time
            }
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _display_loading_results(self, symbol: str, loaded_data: Dict[str, pd.DataFrame], 
                               symbol_info: Dict[str, Any], total_time: float, 
                               memory_used: float, final_memory: float):
        """Display loading results in a formatted way."""
        print(f"\n{Fore.GREEN}✅ Data loaded successfully!")
        print(f"{Fore.CYAN}{'─'*60}")
        print(f"{Fore.YELLOW}📊 Loading Summary:")
        print(f"  • Symbol: {symbol.upper()}")
        print(f"  • Timeframes loaded: {len(loaded_data)}")
        print(f"  • Total rows: {sum(len(df) for df in loaded_data.values()):,}")
        print(f"  • Loading time: {total_time:.2f} seconds")
        print(f"  • Memory used: {memory_used:.1f} MB")
        print(f"  • Total memory: {final_memory:.1f} MB")
        
        # Display timeframe details
        print(f"\n{Fore.YELLOW}📋 Timeframe Details:")
        for tf, df in loaded_data.items():
            tf_info = symbol_info['timeframe_details'][tf]
            print(f"  • {tf:<4}: {len(df):>8,} rows, {tf_info['size_mb']:>6.1f} MB, "
                  f"{tf_info['start_date'][:10]} to {tf_info['end_date'][:10]}")
    
    def _create_mtf_structure(self, loaded_data: Dict[str, pd.DataFrame], symbol: str) -> Dict[str, Any]:
        """Create Multi-Timeframe data structure optimized for ML."""
        try:
            # Determine main timeframe (prefer M1, then M5, then first available)
            main_timeframe = self._determine_main_timeframe(loaded_data)
            
            mtf_data = {
                'symbol': symbol.upper(),
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
                mtf_data['cross_timeframe_features'] = self._create_cross_timeframe_features(
                    loaded_data, main_timeframe)
            
            return mtf_data
            
        except Exception as e:
            print_error(f"Error creating MTF structure: {e}")
            return {'error': str(e)}
    
    def _determine_main_timeframe(self, loaded_data: Dict[str, pd.DataFrame]) -> str:
        """Determine the main timeframe for ML analysis."""
        # Priority order: M1, M5, M15, H1, H4, D1, W1, MN1
        priority_order = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
        
        for tf in priority_order:
            if tf in loaded_data:
                return tf
        
        # If none of the priority timeframes are available, return the first one
        return list(loaded_data.keys())[0] if loaded_data else 'M1'
    
    def _create_cross_timeframe_features(self, loaded_data: Dict[str, pd.DataFrame], 
                                       main_timeframe: str) -> Dict[str, Any]:
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
    
    def _save_loaded_data(self, symbol: str, loaded_data: Dict[str, pd.DataFrame], 
                         mtf_data: Dict[str, Any]):
        """Save loaded data in ML-optimized format."""
        try:
            symbol_mtf_dir = self.mtf_dir / symbol.lower()
            symbol_mtf_dir.mkdir(parents=True, exist_ok=True)
            
            # Save main timeframe data as parquet (most efficient for ML)
            main_tf = mtf_data.get('main_timeframe', 'M1')
            main_data = mtf_data.get('main_data', pd.DataFrame())
            
            if not main_data.empty:
                main_file = symbol_mtf_dir / f"{symbol.lower()}_main_{main_tf.lower()}.parquet"
                main_data.to_parquet(main_file, compression='snappy', index=True)
                print(f"{Fore.GREEN}💾 Main data saved: {main_file}")
            
            # Save cross-timeframe features as separate parquet files
            cross_features = mtf_data.get('cross_timeframe_features', {})
            if cross_features:
                cross_dir = symbol_mtf_dir / "cross_timeframes"
                cross_dir.mkdir(exist_ok=True)
                
                for tf, df in cross_features.items():
                    if not df.empty:
                        cross_file = cross_dir / f"{symbol.lower()}_{tf.lower()}_cross.parquet"
                        df.to_parquet(cross_file, compression='snappy', index=True)
                
                print(f"{Fore.GREEN}💾 Cross-timeframe features saved: {len(cross_features)} files")
            
            # Save lightweight metadata (no heavy data)
            metadata = {
                'symbol': symbol.upper(),
                'main_timeframe': main_tf,
                'timeframes': list(loaded_data.keys()),
                'total_rows': sum(len(df) for df in loaded_data.values()),
                'main_data_shape': list(main_data.shape) if not main_data.empty else [0, 0],
                'cross_timeframes': list(cross_features.keys()),
                'created_at': pd.Timestamp.now().isoformat(),
                'data_path': str(symbol_mtf_dir),
                'main_file': str(main_file) if not main_data.empty else None
            }
            
            metadata_file = symbol_mtf_dir / "mtf_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Create a lightweight loader script
            self._create_ml_loader_script(symbol, metadata, symbol_mtf_dir)
            
            print(f"{Fore.GREEN}💾 MTF structure saved to: {symbol_mtf_dir}")
            
        except Exception as e:
            print_error(f"Error saving loaded data: {e}")
    
    def _create_ml_loader_script(self, symbol: str, metadata: Dict[str, Any], symbol_mtf_dir: Path):
        """Create a lightweight ML loader script."""
        current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        
        loader_script = f'''# -*- coding: utf-8 -*-
"""
ML Data Loader for {symbol.upper()}
Generated on: {current_time}

Lightweight loader for ML analysis with optimized data access.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

class {symbol.upper()}MLLoader:
    """Optimized ML data loader for {symbol.upper()}."""
    
    def __init__(self, data_dir: str = "data/cleaned_data/mtf_structures/{symbol.lower()}"):
        self.data_dir = Path(data_dir)
        self.symbol = "{symbol.upper()}"
        self.main_timeframe = "{metadata['main_timeframe']}"
        
        # Load metadata
        with open(self.data_dir / "mtf_metadata.json", "r") as f:
            self.metadata = json.load(f)
    
    def load_main_data(self) -> pd.DataFrame:
        """Load main timeframe data (optimized for ML)."""
        main_file = self.data_dir / f"{{self.symbol.lower()}}_main_{{self.main_timeframe.lower()}}.parquet"
        return pd.read_parquet(main_file)
    
    def load_cross_timeframe(self, timeframe: str) -> pd.DataFrame:
        """Load cross-timeframe data."""
        cross_file = self.data_dir / "cross_timeframes" / f"{{self.symbol.lower()}}_{{timeframe.lower()}}_cross.parquet"
        return pd.read_parquet(cross_file)
    
    def load_all_cross_timeframes(self) -> dict:
        """Load all cross-timeframe data."""
        cross_data = {{}}
        for tf in self.metadata['cross_timeframes']:
            cross_data[tf] = self.load_cross_timeframe(tf)
        return cross_data
    
    def get_data_info(self) -> dict:
        """Get data information."""
        return self.metadata
    
    def get_ml_ready_data(self) -> dict:
        """Get ML-ready data structure."""
        return {{
            'main_data': self.load_main_data(),
            'cross_timeframes': self.load_all_cross_timeframes(),
            'metadata': self.metadata
        }}

# Example usage:
if __name__ == "__main__":
    loader = {symbol.upper()}MLLoader()
    
    # Load main data
    main_data = loader.load_main_data()
    print(f"Main data shape: {{main_data.shape}}")
    
    # Load all data for ML
    ml_data = loader.get_ml_ready_data()
    print(f"ML data ready: {{len(ml_data['cross_timeframes'])}} cross-timeframes")
'''
        
        with open(symbol_mtf_dir / f"{symbol.lower()}_ml_loader.py", "w") as f:
            f.write(loader_script)
    
    def _show_loading_progress(self, message: str, progress: float = 0.0, 
                             eta: str = "", speed: str = ""):
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
