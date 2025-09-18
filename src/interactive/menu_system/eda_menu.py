# -*- coding: utf-8 -*-
"""
EDA Analysis Menu for NeoZork Interactive ML Trading Strategy Development.

This module provides the EDA analysis submenu with comprehensive data quality checks.
"""

from typing import Dict, Any, Optional
import colorama
import time
import pandas as pd
from colorama import Fore, Back, Style
from .base_menu import BaseMenu
from src.common.logger import print_debug

class EDAMenu(BaseMenu):
    """
    EDA analysis submenu with comprehensive data quality checks.
    
    Features:
    - Time series gaps analysis
    - Duplicates detection
    - NaN values analysis
    - Zero values analysis
    - Negative values analysis
    - Infinity values analysis
    - Outliers detection
    - Basic statistics
    - Correlation analysis
    - EDA report generation
    """
    
    def __init__(self):
        """Initialize the EDA analysis menu."""
        super().__init__()
        self.gaps_analyzer = None
        self.menu_items = {
            "1": {"title": "⏰ Time Series Gaps Analysis", "handler": self._analyze_gaps},
            "2": {"title": "🔄 Duplicates", "handler": self._analyze_duplicates},
            "3": {"title": "❓ NaN Values", "handler": self._analyze_nan},
            "4": {"title": "0️⃣ Zero Values", "handler": self._analyze_zeros},
            "5": {"title": "➖ Negative Values", "handler": self._analyze_negatives},
            "6": {"title": "♾️ Infinity Values", "handler": self._analyze_infinity},
            "7": {"title": "📊 Outliers", "handler": self._analyze_outliers},
            "8": {"title": "📈 Basic Statistics", "handler": self._analyze_basic_stats},
            "9": {"title": "🔗 Correlation Analysis", "handler": self._analyze_correlation},
            "10": {"title": "📊 Generate EDA Report", "handler": self._generate_eda_report},
            "0": {"title": "🔙 Back", "handler": None},
            "00": {"title": "🚪 Exit", "handler": self._exit_system}
        }
    
    def show_menu(self):
        """Display the EDA analysis menu."""
        print(f"\n{Fore.YELLOW}🔍 EDA ANALYSIS")
        print(f"{Fore.CYAN}{'─'*50}")
        
        # Check if data is loaded
        if not self._is_data_loaded():
            print(f"{Fore.RED}⚠️  No data loaded in memory!")
            print(f"{Fore.YELLOW}💡 Please first load data using 'Load Data -> 4.Cleaned Data'")
            print(f"{Fore.CYAN}{'─'*50}")
            print(f"{Fore.RED}0. 🔙 Back")
            print(f"{Fore.RED}00. 🚪 Exit")
            print(f"{Fore.CYAN}{'─'*50}\n")
            return
        
        for key, item in self.menu_items.items():
            if key in ["0", "00"]:
                print(f"{Fore.RED}{key}. {item['title']}")
            else:
                print(f"{Fore.WHITE}{key}. {item['title']}")
        
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.YELLOW}💡 Analyze data quality and generate insights")
        print(f"{Fore.CYAN}{'─'*50}\n")
    
    def _is_data_loaded(self) -> bool:
        """Check if data is loaded in memory."""
        try:
            from src.interactive.data_state_manager import data_state_manager
            return data_state_manager.has_loaded_data()
        except ImportError:
            # Fallback if data_state_manager is not available
            return False
        except Exception:
            return False
    
    def _analyze_gaps(self):
        """Analyze time series gaps."""
        try:
            print(f"\n{Fore.YELLOW}⏰ Time Series Gaps Analysis")
            print(f"{Fore.CYAN}{'─'*50}")
            
            # Get loaded data
            mtf_data = self._get_loaded_data()
            if not mtf_data:
                print(f"{Fore.RED}❌ No data loaded in memory!")
                print(f"{Fore.YELLOW}💡 Please first load data using 'Load Data -> 4.Cleaned Data'")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Initialize gaps analyzer
            if not self.gaps_analyzer:
                from src.interactive.eda_analysis.gaps_analysis import GapsAnalyzer
                self.gaps_analyzer = GapsAnalyzer()
            
            # Show gaps analysis menu
            self._show_gaps_analysis_menu(mtf_data)
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error in gaps analysis: {e}")
            import traceback
            traceback.print_exc()
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _analyze_duplicates(self):
        """Analyze duplicates."""
        print(f"\n{Fore.YELLOW}🔄 Analyzing Duplicates...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _analyze_nan(self):
        """Analyze NaN values."""
        print(f"\n{Fore.YELLOW}❓ Analyzing NaN Values...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _analyze_zeros(self):
        """Analyze zero values."""
        print(f"\n{Fore.YELLOW}0️⃣ Analyzing Zero Values...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _analyze_negatives(self):
        """Analyze negative values."""
        print(f"\n{Fore.YELLOW}➖ Analyzing Negative Values...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _analyze_infinity(self):
        """Analyze infinity values."""
        print(f"\n{Fore.YELLOW}♾️ Analyzing Infinity Values...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _analyze_outliers(self):
        """Analyze outliers."""
        print(f"\n{Fore.YELLOW}📊 Analyzing Outliers...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _analyze_basic_stats(self):
        """Analyze basic statistics."""
        print(f"\n{Fore.YELLOW}📈 Analyzing Basic Statistics...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _analyze_correlation(self):
        """Analyze correlation."""
        print(f"\n{Fore.YELLOW}🔗 Analyzing Correlation...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _generate_eda_report(self):
        """Generate EDA report."""
        print(f"\n{Fore.YELLOW}📊 Generating EDA Report...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _show_gaps_analysis_menu(self, mtf_data: Dict[str, Any]):
        """Show gaps analysis submenu."""
        while True:
            print(f"\n{Fore.YELLOW}🔍 GAPS ANALYSIS MENU")
            print(f"{Fore.CYAN}{'─'*40}")
            print(f"{Fore.WHITE}1. 🔍 Detect Gaps Only")
            print(f"{Fore.WHITE}2. 🔧 Detect & Fix Gaps")
            print(f"{Fore.WHITE}3. 📊 Show Available Strategies")
            print(f"{Fore.WHITE}4. 💾 List Backups")
            print(f"{Fore.WHITE}5. 🔄 Restore from Backup")
            print(f"{Fore.WHITE}6. 🧹 Cleanup Backups")
            print(f"{Fore.RED}0. 🔙 Back")
            print(f"{Fore.CYAN}{'─'*40}")
            
            choice = input(f"{Fore.YELLOW}Enter your choice: ").strip()
            
            if choice == "1":
                self._detect_gaps_only(mtf_data)
            elif choice == "2":
                self._detect_and_fix_gaps(mtf_data)
            elif choice == "3":
                self._show_strategies()
            elif choice == "4":
                self._list_backups()
            elif choice == "5":
                self._restore_from_backup()
            elif choice == "6":
                self._cleanup_backups()
            elif choice == "0":
                break
            else:
                print(f"{Fore.RED}❌ Invalid choice. Please try again.")
    
    def _detect_gaps_only(self, mtf_data: Dict[str, Any]):
        """Detect gaps only without fixing."""
        try:
            print(f"\n{Fore.YELLOW}🔍 Detecting gaps...")
            
            # Get symbol from data
            symbol = mtf_data.get('_symbol', 'UNKNOWN')
            
            # Detect gaps
            gaps_result = self.gaps_analyzer.detector.detect_gaps_in_mtf_data(mtf_data)
            
            if gaps_result['status'] == 'success':
                self._display_gaps_results(gaps_result, symbol)
            else:
                print(f"{Fore.RED}❌ Error detecting gaps: {gaps_result['message']}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error in gaps detection: {e}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _detect_and_fix_gaps(self, mtf_data: Dict[str, Any]):
        """Detect and fix gaps."""
        try:
            print(f"\n{Fore.YELLOW}🔧 Detect & Fix Gaps")
            print(f"{Fore.CYAN}{'─'*30}")
            
            # Get symbol from data
            symbol = mtf_data.get('_symbol', 'UNKNOWN')
            
            # Show available strategies
            strategies = self.gaps_analyzer.get_available_strategies()
            print(f"{Fore.WHITE}Available strategies:")
            for i, strategy in enumerate(strategies, 1):
                print(f"  {i}. {strategy}")
            
            # Get strategy choice
            while True:
                try:
                    choice = input(f"\n{Fore.YELLOW}Select strategy (1-{len(strategies)}): ").strip()
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(strategies):
                        selected_strategy = strategies[choice_idx]
                        break
                    else:
                        print(f"{Fore.RED}❌ Invalid choice. Please try again.")
                except ValueError:
                    print(f"{Fore.RED}❌ Invalid input. Please enter a number.")
            
            # Ask about backup
            create_backup = input(f"\n{Fore.YELLOW}Create backup before fixing? (y/n): ").strip().lower() == 'y'
            
            # Run analysis and fixing
            result = self.gaps_analyzer.analyze_and_fix_gaps(
                mtf_data, symbol, selected_strategy, create_backup
            )
            
            if result['status'] == 'success':
                # Update mtf_data with fixed data
                fixed_data = result['fixing_result'].get('fixed_data', {})
                if fixed_data:
                    print(f"\n{Fore.GREEN}🔄 Updating data with fixed gaps...")
                    for timeframe, fixed_df in fixed_data.items():
                        if timeframe in mtf_data:
                            mtf_data[timeframe] = fixed_df
                            print(f"  ✅ Updated {timeframe}: {fixed_df.shape}")
                    
                    # Update metadata
                    if '_metadata' in mtf_data:
                        mtf_data['_metadata']['gaps_fixed'] = True
                        mtf_data['_metadata']['last_gap_fix'] = pd.Timestamp.now().isoformat()
                        mtf_data['_metadata']['fixing_strategy'] = selected_strategy
                
                # Ensure all timeframes are preserved in mtf_data for saving
                # The fixed_data might not contain all timeframes (e.g., if no gaps were found)
                # So we need to make sure the original mtf_data structure is preserved
                print(f"\n{Fore.CYAN}📊 Preserving all timeframes for saving...")
                for timeframe in mtf_data.keys():
                    if (isinstance(mtf_data[timeframe], pd.DataFrame) and 
                        not timeframe.startswith('_') and 
                        timeframe not in fixed_data):
                        print(f"  ✅ Preserved {timeframe}: {mtf_data[timeframe].shape}")
                
                # Ask where to save fixed data
                print(f"\n{Fore.YELLOW}💾 Where would you like to save the fixed data?")
                print(f"  1. 📁 Original files (overwrite source files)")
                print(f"  2. 🆕 New MTF structure (create new files)")
                print(f"  3. ❌ Don't save")
                
                save_choice = input(f"\n{Fore.CYAN}Enter your choice (1-3): ").strip()
                
                if save_choice == '1':
                    print(f"\n{Fore.GREEN}💾 Saving fixed data to original files...")
                    save_result = self.gaps_analyzer.save_fixed_data_to_original_files(mtf_data, symbol)
                    
                    if save_result['status'] == 'success':
                        print(f"{Fore.GREEN}✅ Fixed data saved to original files!")
                        print(f"  • Symbol: {save_result['symbol']}")
                        print(f"  • Source: {save_result['source']}")
                        if 'saved_files' in save_result:
                            print(f"  • Files updated: {save_result['files_count']}")
                        elif 'mtf_path' in save_result:
                            print(f"  • Path: {save_result['mtf_path']}")
                        print(f"\n{Fore.CYAN}💡 Original files have been updated with fixed data")
                    else:
                        print(f"{Fore.RED}❌ Failed to save to original files: {save_result['message']}")
                
                elif save_choice == '2':
                    print(f"\n{Fore.GREEN}💾 Saving fixed data to new MTF structure...")
                    
                    # Determine original source from metadata
                    original_source = 'gaps_fixed'  # Default fallback
                    if '_metadata' in mtf_data and 'source' in mtf_data['_metadata']:
                        original_source = mtf_data['_metadata']['source']
                    elif '_metadata' in mtf_data and 'data_path' in mtf_data['_metadata']:
                        # Extract source from data_path like "data/cleaned_data/mtf_structures/binance/btcusdt"
                        data_path = mtf_data['_metadata']['data_path']
                        if 'binance' in data_path:
                            original_source = 'binance'
                        elif 'csv' in data_path:
                            original_source = 'csv'
                        # Add more sources as needed
                    
                    # Create source path: gaps_fixed/{original_source}
                    source_path = f"gaps_fixed/{original_source}"
                    save_result = self.gaps_analyzer.save_fixed_data_to_mtf(mtf_data, symbol, source_path)
                    
                    if save_result['status'] == 'success':
                        print(f"{Fore.GREEN}✅ Fixed data saved to new MTF structure!")
                        print(f"  • Path: {save_result['mtf_path']}")
                        print(f"  • Files created: {save_result['files_created']}")
                        print(f"  • Source: {save_result['source']}")
                        print(f"\n{Fore.CYAN}💡 You can now load this data using 'Load Data -> 4. Cleaned Data'")
                    else:
                        print(f"{Fore.RED}❌ Failed to save to MTF structure: {save_result['message']}")
                
                elif save_choice == '3':
                    print(f"{Fore.YELLOW}⏭️  Skipping save - data remains in memory only")
                
                else:
                    print(f"{Fore.RED}❌ Invalid choice - skipping save")
                
                self._display_fixing_results(result)
            else:
                print(f"{Fore.RED}❌ Error in gaps analysis: {result['message']}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error in gaps fixing: {e}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _show_strategies(self):
        """Show available gap filling strategies."""
        try:
            strategies = self.gaps_analyzer.get_available_strategies()
            
            print(f"\n{Fore.YELLOW}📊 Available Gap Filling Strategies")
            print(f"{Fore.CYAN}{'─'*40}")
            
            strategy_descriptions = {
                'auto': '🤖 Auto-select best strategy based on data characteristics',
                'forward_fill': 'Fill gaps with last known value',
                'backward_fill': 'Fill gaps with next known value',
                'linear_interpolation': 'Linear interpolation between values',
                'spline_interpolation': 'Spline interpolation (smooth curves)',
                'mean_fill': 'Fill gaps with mean value',
                'median_fill': 'Fill gaps with median value'
            }
            
            for i, strategy in enumerate(strategies, 1):
                description = strategy_descriptions.get(strategy, 'No description available')
                print(f"{Fore.WHITE}{i:2d}. {strategy:<20} - {description}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error showing strategies: {e}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _list_backups(self):
        """List available backups."""
        try:
            print(f"\n{Fore.YELLOW}💾 Available Backups")
            print(f"{Fore.CYAN}{'─'*30}")
            
            result = self.gaps_analyzer.list_backups()
            
            if result['status'] == 'success' and result['backups']:
                for backup in result['backups']:
                    metadata = backup['metadata']
                    size_mb = backup['backup_size'] / 1024 / 1024
                    print(f"{Fore.WHITE}• {backup['backup_name']}")
                    print(f"  Symbol: {metadata.get('symbol', 'Unknown')}")
                    print(f"  Created: {metadata.get('created_at', 'Unknown')}")
                    print(f"  Size: {size_mb:.2f} MB")
                    print()
            else:
                print(f"{Fore.YELLOW}No backups found.")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error listing backups: {e}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _restore_from_backup(self):
        """Restore data from backup."""
        try:
            print(f"\n{Fore.YELLOW}🔄 Restore from Backup")
            print(f"{Fore.CYAN}{'─'*25}")
            
            # List backups
            result = self.gaps_analyzer.list_backups()
            
            if result['status'] != 'success' or not result['backups']:
                print(f"{Fore.YELLOW}No backups available.")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
                return
            
            # Show backups
            print(f"{Fore.WHITE}Available backups:")
            for i, backup in enumerate(result['backups'], 1):
                metadata = backup['metadata']
                print(f"  {i}. {backup['backup_name']} ({metadata.get('symbol', 'Unknown')})")
            
            # Get backup choice
            while True:
                try:
                    choice = input(f"\n{Fore.YELLOW}Select backup (1-{len(result['backups'])}): ").strip()
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(result['backups']):
                        selected_backup = result['backups'][choice_idx]['backup_name']
                        break
                    else:
                        print(f"{Fore.RED}❌ Invalid choice. Please try again.")
                except ValueError:
                    print(f"{Fore.RED}❌ Invalid input. Please enter a number.")
            
            # Restore backup
            restore_result = self.gaps_analyzer.restore_from_backup(selected_backup)
            
            if restore_result['status'] == 'success':
                print(f"{Fore.GREEN}✅ Backup restored successfully!")
                print(f"Symbol: {restore_result['metadata'].get('symbol', 'Unknown')}")
                print(f"Created: {restore_result['metadata'].get('created_at', 'Unknown')}")
            else:
                print(f"{Fore.RED}❌ Error restoring backup: {restore_result['message']}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error restoring backup: {e}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _cleanup_backups(self):
        """Cleanup old backups."""
        try:
            print(f"\n{Fore.YELLOW}🧹 Cleanup Backups")
            print(f"{Fore.CYAN}{'─'*20}")
            
            keep_count = input(f"{Fore.YELLOW}How many backups to keep? (default: 5): ").strip()
            if not keep_count:
                keep_count = 5
            else:
                keep_count = int(keep_count)
            
            result = self.gaps_analyzer.cleanup_backups(keep_count)
            
            if result['status'] == 'success':
                print(f"{Fore.GREEN}✅ Cleanup completed!")
                print(f"Deleted: {result.get('deleted_count', 0)} backups")
                print(f"Remaining: {result.get('remaining_count', 0)} backups")
            else:
                print(f"{Fore.RED}❌ Error during cleanup: {result['message']}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error during cleanup: {e}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _display_gaps_results(self, gaps_result: Dict[str, Any], symbol: str):
        """Display gaps detection results."""
        try:
            # Try to get actual symbol from metadata
            actual_symbol = symbol
            if isinstance(gaps_result, dict) and 'timeframe_gaps' in gaps_result:
                for tf_data in gaps_result['timeframe_gaps'].values():
                    if isinstance(tf_data, dict) and '_symbol' in tf_data:
                        actual_symbol = tf_data['_symbol']
                        break
            
            print(f"\n{Fore.GREEN}✅ Gaps Detection Results for {actual_symbol}")
            print(f"{Fore.CYAN}{'─'*50}")
            
            overall_stats = gaps_result.get('overall_stats', {})
            
            print(f"{Fore.WHITE}Overall Statistics:")
            print(f"  • Total gaps: {overall_stats.get('total_gaps_across_timeframes', 0)}")
            print(f"  • Missing points: {overall_stats.get('total_missing_points_across_timeframes', 0)}")
            print(f"  • Timeframes with gaps: {overall_stats.get('timeframes_with_gaps', 0)}")
            print(f"  • Total gap duration: {overall_stats.get('total_gap_duration_seconds', 0) / 3600:.2f} hours")
            print(f"  • Gaps percentage: {overall_stats.get('gaps_percentage', 0):.1f}%")
            
            # Show per-timeframe results
            timeframe_gaps = gaps_result.get('timeframe_gaps', {})
            if timeframe_gaps:
                print(f"\n{Fore.WHITE}Per-Timeframe Results:")
                for timeframe, result in timeframe_gaps.items():
                    if result.get('status') == 'success':
                        stats = result.get('statistics', {})
                        actual_interval = result.get('actual_interval', 'Unknown')
                        expected_interval = result.get('expected_interval', 'Unknown')
                        
                        # Show interval mismatch warning only if there's a mismatch
                        is_mismatch = result.get('is_interval_mismatch', False)
                        if is_mismatch:
                            if timeframe == 'M1':
                                print(f"  • {timeframe}: {stats.get('total_gaps', 0)} gaps, "
                                      f"{stats.get('total_missing_points', 0)} missing points")
                            elif timeframe == 'MN1':
                                # MN1 can have 28-31 day intervals, which is normal for monthly data
                                print(f"  • {timeframe}: {stats.get('total_gaps', 0)} gaps, "
                                      f"{stats.get('total_missing_points', 0)} missing points")
                            else:
                                print(f"  • {timeframe}: {stats.get('total_gaps', 0)} gaps, "
                                      f"{stats.get('total_missing_points', 0)} missing points "
                                      f"(⚠️  Synthetic data - {actual_interval} intervals, expected {expected_interval})")
                        else:
                            print(f"  • {timeframe}: {stats.get('total_gaps', 0)} gaps, "
                                  f"{stats.get('total_missing_points', 0)} missing points")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error displaying results: {e}")
    
    def _display_fixing_results(self, result: Dict[str, Any]):
        """Display gaps fixing results."""
        try:
            print(f"\n{Fore.GREEN}✅ Gaps Fixing Results")
            print(f"{Fore.CYAN}{'─'*30}")
            
            summary = result.get('summary', {})
            overall_stats = result.get('overall_stats', {})
            
            print(f"{Fore.WHITE}Summary:")
            print(f"  • Gaps detected: {summary.get('gaps_detected', 0)}")
            print(f"  • Gaps fixed: {summary.get('gaps_fixed', 0)}")
            print(f"  • Points added: {summary.get('points_added', 0)}")
            print(f"  • Timeframes fixed: {summary.get('timeframes_fixed', 0)}")
            print(f"  • Timeframes skipped: {overall_stats.get('timeframes_skipped', 0)}")
            print(f"  • Success rate: {summary.get('fixing_success_rate', 0):.1f}%")
            print(f"  • Strategy used: {result.get('strategy_used', 'Unknown')}")
            
            if result.get('backup_created'):
                print(f"  • Backup created: Yes")
            else:
                print(f"  • Backup created: No")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error displaying fixing results: {e}")
    
    def _get_loaded_data(self) -> Optional[Dict[str, Any]]:
        """Get loaded data from data state manager."""
        try:
            from src.interactive.data_state_manager import data_state_manager
            data = data_state_manager.get_loaded_data()
            
            # Debug: Print data structure info
            if data:
                print_debug(f"Loaded data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, dict):
                            print_debug(f"  {key}: {list(value.keys())}")
                        else:
                            print_debug(f"  {key}: {type(value)}")
            else:
                print_debug("No data loaded in data_state_manager")
                return None
            
            # Convert data structure for gaps analysis
            converted_data = self._convert_data_for_gaps_analysis(data)
            return converted_data
            
        except ImportError:
            print_debug("data_state_manager not available")
            return None
        except Exception as e:
            print_debug(f"Error getting loaded data: {e}")
            return None
    
    def _convert_data_for_gaps_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert loaded data structure to format expected by gaps analysis.
        
        Args:
            data: Raw data from data_state_manager
            
        Returns:
            Converted data structure for gaps analysis
        """
        try:
            if not data or 'main_data' not in data:
                return data
            
            # Get main data and cross timeframes
            main_data = data['main_data']
            metadata = data.get('metadata', {})
            cross_timeframes_data = data.get('cross_timeframes', {})  # This should be a dict with data
            cross_timeframes_list = metadata.get('cross_timeframes', [])  # This is a list of names
            
            # Create gaps analysis structure
            converted_data = {}
            
            # Add main timeframe data
            if 'main_timeframe' in metadata:
                main_tf = metadata['main_timeframe']
                converted_data[main_tf] = main_data
                print_debug(f"Added main timeframe {main_tf}: {main_data.shape}")
            
            # Add cross timeframes data
            for tf in cross_timeframes_list:
                if tf in cross_timeframes_data:
                    # Data is already loaded in memory
                    converted_data[tf] = cross_timeframes_data[tf]
                    print_debug(f"Added cross timeframe {tf}: {cross_timeframes_data[tf].shape}")
                else:
                    # Try to load cross timeframe data from disk
                    try:
                        cross_data = self._load_cross_timeframe_data(metadata.get('symbol', 'UNKNOWN'), tf, metadata.get('source', 'unknown'))
                        if cross_data is not None:
                            converted_data[tf] = cross_data
                            print_debug(f"Loaded cross timeframe {tf} from disk: {cross_data.shape}")
                        else:
                            print_debug(f"Could not load cross timeframe {tf} from disk")
                    except Exception as e:
                        print_debug(f"Error loading cross timeframe {tf}: {e}")
            
            # Add metadata
            converted_data['_metadata'] = metadata
            converted_data['_symbol'] = metadata.get('symbol', 'UNKNOWN')
            
            print_debug(f"Converted data structure: {list(converted_data.keys())}")
            return converted_data
            
        except Exception as e:
            print_debug(f"Error converting data for gaps analysis: {e}")
            return data
    
    def _load_cross_timeframe_data(self, symbol: str, timeframe: str, source: str = 'unknown') -> Optional[pd.DataFrame]:
        """
        Load cross timeframe data from disk.
        
        Args:
            symbol: Symbol name
            timeframe: Timeframe to load
            source: Data source (e.g., 'binance', 'csv')
            
        Returns:
            DataFrame with cross timeframe data or None if not found
        """
        try:
            from pathlib import Path
            import pandas as pd
            
            # Try different possible paths for cross timeframe data
            possible_paths = [
                # MTF structure path with source
                Path(f"data/cleaned_data/mtf_structures/{source}/{symbol.lower()}/cross_timeframes/{symbol.lower()}_{timeframe.lower()}_cross.parquet"),
                # Fallback paths
                Path(f"data/cleaned_data/mtf_structures/csv/{symbol.lower()}/cross_timeframes/{symbol.lower()}_{timeframe.lower()}_cross.parquet"),
                Path(f"data/cleaned_data/{symbol.lower()}/cross_timeframes/{symbol.lower()}_{timeframe.lower()}_cross.parquet"),
                Path(f"data/cleaned_data/{symbol.lower()}/{symbol.lower()}_{timeframe.lower()}.parquet"),
                Path(f"data/cleaned_data/{symbol.lower()}/{timeframe.lower()}.parquet"),
            ]
            
            for path in possible_paths:
                if path.exists():
                    print_debug(f"Loading cross timeframe data from: {path}")
                    df = pd.read_parquet(path)
                    return df
            
            print_debug(f"Cross timeframe data not found for {symbol} {timeframe} in source {source}")
            return None
            
        except Exception as e:
            print_debug(f"Error loading cross timeframe data: {e}")
            return None
