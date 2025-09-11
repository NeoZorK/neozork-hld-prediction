# -*- coding: utf-8 -*-
"""
Configuration Menu for NeoZork Interactive ML Trading Strategy Development.

This module provides the system configuration submenu with comprehensive
system information, loaded data status, and configuration options.
"""

import os
import sys
import time
import psutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import colorama
from colorama import Fore, Back, Style
from .base_menu import BaseMenu

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug


class ConfigurationMenu(BaseMenu):
    """
    System configuration submenu with comprehensive system information.
    
    Features:
    - System status and information
    - Loaded data status
    - Memory usage monitoring
    - Data range information
    - Configuration options
    - System health monitoring
    """
    
    def __init__(self):
        """Initialize the configuration menu."""
        super().__init__()
        self.menu_items = {
            "1": {"title": "📊 System Status", "handler": self._system_status},
            "2": {"title": "💾 Loaded Data Status", "handler": self._loaded_data_status},
            "3": {"title": "🧠 Memory Usage", "handler": self._memory_usage},
            "4": {"title": "📅 Data Range Information", "handler": self._data_range_info},
            "5": {"title": "⚙️ Configuration Options", "handler": self._configuration_options},
            "6": {"title": "🔧 System Health", "handler": self._system_health},
            "0": {"title": "🔙 Back", "handler": None},
            "00": {"title": "🚪 Exit", "handler": self._exit_system}
        }
    
    def show_menu(self):
        """Display the configuration menu."""
        print(f"\n{Fore.YELLOW}⚙️ SYSTEM CONFIGURATION")
        print(f"{Fore.CYAN}{'─'*50}")
        
        for key, item in self.menu_items.items():
            if key in ["0", "00"]:
                print(f"{Fore.RED}{key}. {item['title']}")
            else:
                print(f"{Fore.WHITE}{key}. {item['title']}")
        
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.YELLOW}💡 Monitor system status and configuration")
        print(f"{Fore.CYAN}{'─'*50}\n")
    
    def _system_status(self):
        """Display comprehensive system status."""
        print(f"\n{Fore.YELLOW}📊 System Status")
        print(f"{Fore.CYAN}{'─'*60}")
        
        try:
            # System information
            print(f"{Fore.GREEN}🖥️  System Information:")
            print(f"  • OS: {os.name}")
            print(f"  • Python: {sys.version.split()[0]}")
            print(f"  • Platform: {sys.platform}")
            print(f"  • Working Directory: {os.getcwd()}")
            
            # Process information
            process = psutil.Process()
            print(f"\n{Fore.GREEN}🔄 Process Information:")
            print(f"  • PID: {process.pid}")
            print(f"  • CPU Usage: {process.cpu_percent():.1f}%")
            print(f"  • Memory Usage: {process.memory_info().rss / (1024 * 1024):.1f} MB")
            print(f"  • Threads: {process.num_threads()}")
            
            # System resources
            print(f"\n{Fore.GREEN}💻 System Resources:")
            print(f"  • CPU Count: {psutil.cpu_count()}")
            print(f"  • Total Memory: {psutil.virtual_memory().total / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Available Memory: {psutil.virtual_memory().available / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Memory Usage: {psutil.virtual_memory().percent:.1f}%")
            
            # Disk usage
            disk_usage = psutil.disk_usage('/')
            print(f"  • Disk Total: {disk_usage.total / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Disk Used: {disk_usage.used / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Disk Free: {disk_usage.free / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Disk Usage: {(disk_usage.used / disk_usage.total) * 100:.1f}%")
            
        except Exception as e:
            print_error(f"Error getting system status: {e}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _loaded_data_status(self):
        """Display available MTF data status (NOT loaded in memory)."""
        print(f"\n{Fore.YELLOW}💾 Available MTF Data Status")
        print(f"{Fore.CYAN}{'─'*60}")
        print(f"{Fore.YELLOW}💡 This shows available MTF structures, NOT loaded data in memory")
        print(f"{Fore.CYAN}{'─'*60}")
        
        try:
            # Check for MTF structures
            mtf_dir = Path("data/cleaned_data/mtf_structures")
            
            if not mtf_dir.exists():
                print(f"{Fore.RED}❌ No MTF structures found")
                print(f"{Fore.YELLOW}💡 Please create MTF data using 'Load Data -> CSV Converted' first")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Get all source directories
            source_dirs = [f for f in mtf_dir.iterdir() if f.is_dir()]
            
            if not source_dirs:
                print(f"{Fore.RED}❌ No MTF source directories found")
                print(f"{Fore.YELLOW}💡 Please create MTF data using 'Load Data -> CSV Converted' first")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Get all symbol MTF folders from all source directories
            mtf_symbol_folders = []
            for source_dir in source_dirs:
                symbol_folders = [f for f in source_dir.iterdir() if f.is_dir()]
                for symbol_folder in symbol_folders:
                    # Store source information
                    folder_info = {
                        'path': symbol_folder,
                        'source': source_dir.name
                    }
                    mtf_symbol_folders.append(folder_info)
            
            if not mtf_symbol_folders:
                print(f"{Fore.RED}❌ No MTF symbol folders found")
                print(f"{Fore.YELLOW}💡 Please create MTF data using 'Load Data -> CSV Converted' first")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            print(f"{Fore.GREEN}📈 Available MTF Structures ({len(mtf_symbol_folders)}):")
            print(f"{Fore.CYAN}{'─'*80}")
            print(f"{Fore.WHITE}{'Symbol':<12} {'Source':<10} {'Status':<12} {'Size (MB)':<10} {'Timeframes':<15} {'Created':<15}")
            print(f"{Fore.CYAN}{'─'*80}")
            
            total_size = 0
            for folder_info in sorted(mtf_symbol_folders, key=lambda x: (x['source'], x['path'].name)):
                symbol_folder = folder_info['path']
                source_name = folder_info['source']
                symbol_name = symbol_folder.name.upper()
                mtf_metadata_file = symbol_folder / "mtf_metadata.json"
                
                if mtf_metadata_file.exists():
                    try:
                        with open(mtf_metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        # Calculate folder size
                        folder_size = sum(f.stat().st_size for f in symbol_folder.rglob('*') if f.is_file())
                        folder_size_mb = folder_size / (1024 * 1024)
                        total_size += folder_size_mb
                        
                        # Get timeframes
                        timeframes = metadata.get('timeframes', [])
                        timeframes_str = ', '.join(timeframes[:3])
                        if len(timeframes) > 3:
                            timeframes_str += f" +{len(timeframes)-3} more"
                        
                        # Get creation date
                        created_at = metadata.get('created_at', 'Unknown')
                        if created_at != 'Unknown':
                            try:
                                created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                                created_date = created_dt.strftime('%Y-%m-%d %H:%M')
                            except:
                                created_date = created_at[:16]
                        else:
                            created_date = 'Unknown'
                        
                        print(f"{Fore.WHITE}{symbol_name:<12} {source_name:<10} {'✅ Available':<12} {folder_size_mb:<10.1f} {timeframes_str:<15} {created_date:<15}")
                        
                    except Exception as e:
                        print_error(f"Error reading metadata for {symbol_name}: {e}")
                        print(f"{Fore.WHITE}{symbol_name:<12} {source_name:<10} {'❌ Error':<12} {'0.0':<10} {'Unknown':<15} {'Unknown':<15}")
                else:
                    print(f"{Fore.WHITE}{symbol_name:<12} {source_name:<10} {'⚠️  No Meta':<12} {'0.0':<10} {'Unknown':<15} {'Unknown':<15}")
            
            print(f"{Fore.CYAN}{'─'*80}")
            print(f"{Fore.YELLOW}Total: {len(mtf_symbol_folders)} MTF structures, {total_size:.1f} MB")
            print(f"{Fore.CYAN}💡 Use 'Load Data -> 4.Cleaned Data' to load data into memory")
            
        except Exception as e:
            print_error(f"Error getting MTF data status: {e}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _memory_usage(self):
        """Display detailed memory usage information."""
        print(f"\n{Fore.YELLOW}🧠 Memory Usage")
        print(f"{Fore.CYAN}{'─'*60}")
        
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            # Process memory
            print(f"{Fore.GREEN}🔄 Process Memory:")
            print(f"  • RSS (Resident Set Size): {memory_info.rss / (1024 * 1024):.1f} MB")
            print(f"  • VMS (Virtual Memory Size): {memory_info.vms / (1024 * 1024):.1f} MB")
            print(f"  • Memory Percent: {process.memory_percent():.1f}%")
            
            # System memory
            system_memory = psutil.virtual_memory()
            print(f"\n{Fore.GREEN}💻 System Memory:")
            print(f"  • Total: {system_memory.total / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Available: {system_memory.available / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Used: {system_memory.used / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Free: {system_memory.free / (1024 * 1024 * 1024):.1f} GB")
            print(f"  • Usage: {system_memory.percent:.1f}%")
            
            # Note about loaded data
            print(f"\n{Fore.YELLOW}💡 Note: This shows system memory usage, not loaded data in memory")
            print(f"{Fore.CYAN}💡 Use 'Load Data -> 4.Cleaned Data' to load data into memory")
            
        except Exception as e:
            print_error(f"Error getting memory usage: {e}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    
    def _data_range_info(self):
        """Display data range information for available MTF structures."""
        print(f"\n{Fore.YELLOW}📅 MTF Data Range Information")
        print(f"{Fore.CYAN}{'─'*60}")
        print(f"{Fore.YELLOW}💡 This shows available MTF structures, NOT loaded data in memory")
        print(f"{Fore.CYAN}{'─'*60}")
        
        try:
            mtf_dir = Path("data/cleaned_data/mtf_structures")
            
            if not mtf_dir.exists():
                print(f"{Fore.RED}❌ No MTF structures found")
                print(f"{Fore.YELLOW}💡 Please create MTF data using 'Load Data -> CSV Converted' first")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Get all symbol MTF folders
            mtf_symbol_folders = [f for f in mtf_dir.iterdir() if f.is_dir()]
            
            if not mtf_symbol_folders:
                print(f"{Fore.RED}❌ No MTF structures found")
                print(f"{Fore.YELLOW}💡 Please create MTF data using 'Load Data -> CSV Converted' first")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            for symbol_folder in sorted(mtf_symbol_folders):
                symbol_name = symbol_folder.name.upper()
                mtf_metadata_file = symbol_folder / "mtf_metadata.json"
                
                if mtf_metadata_file.exists():
                    try:
                        with open(mtf_metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        print(f"\n{Fore.GREEN}📈 {symbol_name} (Available MTF Structure):")
                        print(f"  • Main Timeframe: {metadata.get('main_timeframe', 'Unknown')}")
                        print(f"  • Available Timeframes: {', '.join(metadata.get('timeframes', []))}")
                        print(f"  • Total Rows: {metadata.get('total_rows', 0):,}")
                        print(f"  • Main Data Shape: {metadata.get('main_data_shape', [0, 0])}")
                        print(f"  • Cross-timeframes: {len(metadata.get('cross_timeframes', []))}")
                        print(f"  • Created: {metadata.get('created_at', 'Unknown')}")
                        
                        # Try to get actual date range from main data file
                        main_tf = metadata.get('main_timeframe', 'M1').lower()
                        main_file = symbol_folder / f"{symbol_name.lower()}_main_{main_tf}.parquet"
                        
                        if main_file.exists():
                            try:
                                import pandas as pd
                                df = pd.read_parquet(main_file)
                                if not df.empty and hasattr(df.index, 'min'):
                                    start_date = df.index.min().strftime('%Y-%m-%d %H:%M')
                                    end_date = df.index.max().strftime('%Y-%m-%d %H:%M')
                                    print(f"  • Date Range: {start_date} to {end_date}")
                                    print(f"  • Duration: {(df.index.max() - df.index.min()).days} days")
                            except Exception as e:
                                print(f"  • Date Range: Unable to read ({e})")
                        else:
                            print(f"  • Date Range: Main data file not found")
                        
                        print(f"  • Status: {Fore.YELLOW}Available (not loaded in memory)")
                        
                    except Exception as e:
                        print_error(f"Error reading metadata for {symbol_name}: {e}")
                        print(f"{Fore.WHITE}  • Status: Error reading metadata")
                else:
                    print(f"\n{Fore.GREEN}📈 {symbol_name}:")
                    print(f"  • Status: No metadata found")
            
            print(f"\n{Fore.CYAN}💡 Use 'Load Data -> 4.Cleaned Data' to load data into memory")
            
        except Exception as e:
            print_error(f"Error getting data range information: {e}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _configuration_options(self):
        """Display configuration options."""
        print(f"\n{Fore.YELLOW}⚙️ Configuration Options")
        print(f"{Fore.CYAN}{'─'*60}")
        
        print(f"{Fore.GREEN}🔧 Available Options:")
        print(f"  • Data loading settings")
        print(f"  • ML model parameters")
        print(f"  • Backtesting configuration")
        print(f"  • Monitoring settings")
        print(f"  • Alert thresholds")
        print(f"  • Performance tuning")
        
        print(f"\n{Fore.YELLOW}💡 Configuration files location:")
        print(f"  • Project root: {PROJECT_ROOT}")
        print(f"  • Config files: {PROJECT_ROOT / 'config'}")
        print(f"  • Data directory: {PROJECT_ROOT / 'data'}")
        print(f"  • Logs directory: {PROJECT_ROOT / 'logs'}")
        
        print(f"\n{Fore.CYAN}Note: Configuration options will be implemented in future versions.")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _system_health(self):
        """Display system health information."""
        print(f"\n{Fore.YELLOW}🔧 System Health")
        print(f"{Fore.CYAN}{'─'*60}")
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"{Fore.GREEN}🖥️  CPU Health:")
            print(f"  • CPU Usage: {cpu_percent:.1f}%")
            if cpu_percent < 50:
                print(f"  • Status: {Fore.GREEN}✅ Healthy")
            elif cpu_percent < 80:
                print(f"  • Status: {Fore.YELLOW}⚠️  Moderate Load")
            else:
                print(f"  • Status: {Fore.RED}❌ High Load")
            
            # Memory usage
            memory = psutil.virtual_memory()
            print(f"\n{Fore.GREEN}🧠 Memory Health:")
            print(f"  • Memory Usage: {memory.percent:.1f}%")
            if memory.percent < 70:
                print(f"  • Status: {Fore.GREEN}✅ Healthy")
            elif memory.percent < 90:
                print(f"  • Status: {Fore.YELLOW}⚠️  Moderate Usage")
            else:
                print(f"  • Status: {Fore.RED}❌ High Usage")
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            print(f"\n{Fore.GREEN}💾 Disk Health:")
            print(f"  • Disk Usage: {disk_percent:.1f}%")
            if disk_percent < 80:
                print(f"  • Status: {Fore.GREEN}✅ Healthy")
            elif disk_percent < 95:
                print(f"  • Status: {Fore.YELLOW}⚠️  Moderate Usage")
            else:
                print(f"  • Status: {Fore.RED}❌ High Usage")
            
            # Overall health
            print(f"\n{Fore.GREEN}🎯 Overall System Health:")
            if cpu_percent < 50 and memory.percent < 70 and disk_percent < 80:
                print(f"  • Status: {Fore.GREEN}✅ Excellent")
            elif cpu_percent < 80 and memory.percent < 90 and disk_percent < 95:
                print(f"  • Status: {Fore.YELLOW}⚠️  Good")
            else:
                print(f"  • Status: {Fore.RED}❌ Needs Attention")
            
        except Exception as e:
            print_error(f"Error getting system health: {e}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
