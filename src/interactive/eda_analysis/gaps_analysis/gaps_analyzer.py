# -*- coding: utf-8 -*-
"""
Gaps Analyzer for NeoZork Interactive ML Trading Strategy Development.

This module provides the main interface for gaps analysis and fixing.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from src.common.logger import print_info, print_warning, print_error, print_debug

from .gaps_detector import GapsDetector
from .gaps_fixer import GapsFixer
from .progress_tracker import ProgressTracker, MultiProgressTracker
from .backup_manager import BackupManager


class GapsAnalyzer:
    """
    Main gaps analyzer for MTF data.
    
    Features:
    - Complete gaps analysis workflow
    - Progress tracking with ETA
    - Backup management
    - Multiple fixing strategies
    - Comprehensive reporting
    """
    
    def __init__(self):
        """Initialize the gaps analyzer."""
        self.detector = GapsDetector()
        self.fixer = GapsFixer()
        self.backup_manager = BackupManager()
        self.available_strategies = list(self.fixer.filling_strategies.keys())
    
    def _extract_loaded_data(self, mtf_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract loaded data from MTF structure, handling different formats.
        
        Args:
            mtf_data: MTF data structure
            
        Returns:
            Dictionary containing timeframe data
        """
        # Try different possible data structures
        loaded_data = None
        if 'loaded_data' in mtf_data:
            loaded_data = mtf_data['loaded_data']
        elif isinstance(mtf_data, dict):
            # Check if mtf_data itself contains timeframe data (DataFrames)
            timeframe_keys = []
            for k, v in mtf_data.items():
                if (isinstance(v, pd.DataFrame) and 
                    hasattr(v, 'index') and 
                    hasattr(v, 'columns') and
                    not k.startswith('_')):
                    timeframe_keys.append(k)
            
            if timeframe_keys:
                loaded_data = {k: mtf_data[k] for k in timeframe_keys}
                print_debug(f"Extracted timeframes: {timeframe_keys}")
        
        if not loaded_data:
            raise ValueError('No valid timeframe data found in MTF structure')
        
        return loaded_data
    
    def analyze_and_fix_gaps(self, mtf_data: Dict[str, Any], 
                           symbol: str,
                           strategy: str = 'auto',
                           create_backup: bool = True,
                           show_progress: bool = False) -> Dict[str, Any]:
        """
        Complete gaps analysis and fixing workflow.
        
        Args:
            mtf_data: MTF data structure
            symbol: Symbol name
            strategy: Gap filling strategy
            create_backup: Whether to create backup before fixing
            show_progress: Whether to show progress updates
            
        Returns:
            Dictionary containing analysis and fixing results
        """
        try:
            print_info(f"🔍 Starting complete gaps analysis for {symbol}...")
            
            # Debug: Print data structure info
            print_debug(f"MTF data keys: {list(mtf_data.keys()) if isinstance(mtf_data, dict) else 'Not a dict'}")
            if isinstance(mtf_data, dict):
                for key, value in mtf_data.items():
                    if isinstance(value, pd.DataFrame):
                        print_debug(f"  {key}: DataFrame {value.shape}")
                    elif isinstance(value, dict):
                        print_debug(f"  {key}: dict with keys {list(value.keys())}")
                    else:
                        print_debug(f"  {key}: {type(value)}")
            
            # Extract symbol from metadata if available
            if isinstance(mtf_data, dict) and '_symbol' in mtf_data:
                actual_symbol = mtf_data['_symbol']
                print_debug(f"Using symbol from _symbol: {actual_symbol}")
                # Update symbol parameter if it's different
                if actual_symbol != symbol:
                    print_debug(f"Symbol mismatch: parameter='{symbol}', metadata='{actual_symbol}'")
                    symbol = actual_symbol
            elif isinstance(mtf_data, dict) and '_metadata' in mtf_data:
                metadata = mtf_data['_metadata']
                if 'symbol' in metadata:
                    actual_symbol = metadata['symbol']
                    print_debug(f"Using symbol from _metadata: {actual_symbol}")
                    if actual_symbol != symbol:
                        print_debug(f"Symbol mismatch: parameter='{symbol}', metadata='{actual_symbol}'")
                        symbol = actual_symbol
                else:
                    print_debug("No symbol found in _metadata")
            else:
                print_debug("No _symbol or _metadata found in mtf_data")
            
            # Validate inputs
            if not mtf_data:
                return {'status': 'error', 'message': 'No MTF data provided'}
            
            if strategy not in self.available_strategies:
                return {'status': 'error', 'message': f'Unknown strategy: {strategy}'}
            
            # Phase 1: Create backup
            backup_result = None
            if create_backup:
                print_info(f"💾 Creating backup...")
                backup_result = self.backup_manager.create_backup(
                    mtf_data, symbol, "Pre-gap-fixing backup"
                )
                print_info(f"✅ Backup created successfully")
            
            # Phase 2: Detect gaps
            print_info(f"🔍 Detecting gaps...")
            gaps_result = self.detector.detect_gaps_in_mtf_data(mtf_data)
            print_info(f"✅ Gaps detection completed")
            
            if gaps_result['status'] != 'success':
                return gaps_result
            
            # Phase 3: Fix gaps
            print_info(f"🔧 Fixing gaps using strategy: {strategy}...")
            fix_result = self.fixer.fix_gaps_in_mtf_data(
                mtf_data, gaps_result, strategy
            )
            print_info(f"✅ Gaps fixing completed")
            
            # Combine results
            result = {
                'status': 'success',
                'symbol': symbol,
                'strategy_used': strategy,
                'backup_created': backup_result is not None,
                'backup_info': backup_result,
                'gaps_analysis': gaps_result,
                'fixing_result': fix_result,
                'summary': self._create_summary(gaps_result, fix_result)
            }
            
            return result
            
        except Exception as e:
            print_error(f"Error in complete gaps analysis: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _detect_gaps_with_progress(self, mtf_data: Dict[str, Any], 
                                 progress_tracker: ProgressTracker) -> Dict[str, Any]:
        """
        Detect gaps with progress tracking.
        
        Args:
            mtf_data: MTF data structure
            progress_tracker: Progress tracker
            
        Returns:
            Dictionary containing gaps detection results
        """
        try:
            loaded_data = self._extract_loaded_data(mtf_data)
            total_timeframes = len(loaded_data)
            
            # Create progress callback
            def progress_callback(current, total, message):
                progress_tracker.update(current + 1, message)
            
            # Detect gaps
            gaps_result = self.detector.detect_gaps_in_mtf_data(
                mtf_data, progress_callback
            )
            
            return gaps_result
            
        except Exception as e:
            print_error(f"Error in gaps detection with progress: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _fix_gaps_with_progress(self, mtf_data: Dict[str, Any], 
                              gaps_info: Dict[str, Any],
                              strategy: str,
                              progress_tracker: ProgressTracker) -> Dict[str, Any]:
        """
        Fix gaps with progress tracking.
        
        Args:
            mtf_data: MTF data structure
            gaps_info: Gap information
            strategy: Fixing strategy
            progress_tracker: Progress tracker
            
        Returns:
            Dictionary containing fixing results
        """
        try:
            loaded_data = self._extract_loaded_data(mtf_data)
            total_timeframes = len(loaded_data)
            
            # Create progress callback
            def progress_callback(current, total, message):
                progress_tracker.update(current + 1, message)
            
            # Fix gaps
            fix_result = self.fixer.fix_gaps_in_mtf_data(
                mtf_data, gaps_info, strategy, progress_callback
            )
            
            return fix_result
            
        except Exception as e:
            print_error(f"Error in gaps fixing with progress: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _create_summary(self, gaps_result: Dict[str, Any], 
                       fix_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create summary of gaps analysis and fixing.
        
        Args:
            gaps_result: Gaps detection results
            fix_result: Gaps fixing results
            
        Returns:
            Dictionary containing summary
        """
        try:
            gaps_stats = gaps_result.get('overall_stats', {})
            fix_stats = fix_result.get('overall_stats', {})
            
            summary = {
                'gaps_detected': gaps_stats.get('total_gaps_across_timeframes', 0),
                'missing_points': gaps_stats.get('total_missing_points_across_timeframes', 0),
                'timeframes_with_gaps': gaps_stats.get('timeframes_with_gaps', 0),
                'gaps_fixed': fix_stats.get('total_gaps_fixed', 0),
                'points_added': fix_stats.get('total_points_added', 0),
                'timeframes_fixed': fix_stats.get('timeframes_fixed', 0),
                'fixing_success_rate': fix_stats.get('fixing_success_rate', 0),
                'total_gap_duration_hours': gaps_stats.get('total_gap_duration_seconds', 0) / 3600
            }
            
            return summary
            
        except Exception as e:
            print_error(f"Error creating summary: {e}")
            return {
                'gaps_detected': 0,
                'missing_points': 0,
                'timeframes_with_gaps': 0,
                'gaps_fixed': 0,
                'points_added': 0,
                'timeframes_fixed': 0,
                'fixing_success_rate': 0,
                'total_gap_duration_hours': 0
            }
    
    def get_available_strategies(self) -> List[str]:
        """
        Get list of available gap filling strategies.
        
        Returns:
            List of strategy names
        """
        return self.available_strategies.copy()
    
    def restore_from_backup(self, backup_name: str) -> Dict[str, Any]:
        """
        Restore data from backup.
        
        Args:
            backup_name: Name of the backup to restore
            
        Returns:
            Dictionary containing restored data
        """
        try:
            print_info(f"🔄 Restoring data from backup: {backup_name}...")
            
            restore_result = self.backup_manager.restore_backup(backup_name)
            
            if restore_result['status'] == 'success':
                print_info(f"✅ Data restored from backup: {backup_name}")
            else:
                print_error(f"❌ Failed to restore from backup: {restore_result['message']}")
            
            return restore_result
            
        except Exception as e:
            print_error(f"Error restoring from backup: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def list_backups(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        List available backups.
        
        Args:
            symbol: Optional symbol filter
            
        Returns:
            Dictionary containing backup list
        """
        try:
            return self.backup_manager.list_backups(symbol)
        except Exception as e:
            print_error(f"Error listing backups: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def cleanup_backups(self, keep_count: int = 5) -> Dict[str, Any]:
        """
        Clean up old backups.
        
        Args:
            keep_count: Number of backups to keep
            
        Returns:
            Dictionary containing cleanup result
        """
        try:
            return self.backup_manager.cleanup_old_backups(keep_count)
        except Exception as e:
            print_error(f"Error cleaning up backups: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def validate_mtf_data(self, mtf_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate MTF data structure.
        
        Args:
            mtf_data: MTF data to validate
            
        Returns:
            Dictionary containing validation result
        """
        try:
            if not mtf_data:
                return {'status': 'error', 'message': 'No data provided'}
            
            # Try to extract loaded data using the same logic as other methods
            try:
                loaded_data = self._extract_loaded_data(mtf_data)
            except ValueError as e:
                return {'status': 'error', 'message': str(e)}
            if not loaded_data:
                return {'status': 'error', 'message': 'No timeframes in loaded_data'}
            
            validation_results = {}
            total_rows = 0
            
            for timeframe, df in loaded_data.items():
                if not isinstance(df, pd.DataFrame):
                    validation_results[timeframe] = {
                        'status': 'error',
                        'message': 'Not a DataFrame'
                    }
                    continue
                
                if df.empty:
                    validation_results[timeframe] = {
                        'status': 'warning',
                        'message': 'Empty DataFrame'
                    }
                    continue
                
                if not isinstance(df.index, pd.DatetimeIndex):
                    validation_results[timeframe] = {
                        'status': 'error',
                        'message': 'Index is not DatetimeIndex'
                    }
                    continue
                
                total_rows += len(df)
                validation_results[timeframe] = {
                    'status': 'success',
                    'rows': len(df),
                    'columns': len(df.columns),
                    'time_span': {
                        'start': df.index.min().isoformat(),
                        'end': df.index.max().isoformat()
                    }
                }
            
            return {
                'status': 'success',
                'timeframes': validation_results,
                'total_timeframes': len(loaded_data),
                'total_rows': total_rows
            }
            
        except Exception as e:
            print_error(f"Error validating MTF data: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def save_fixed_data_to_original_files(self, mtf_data: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """
        Save fixed data back to original files.
        
        Args:
            mtf_data: MTF data structure with fixed data
            symbol: Symbol name
            
        Returns:
            Dictionary containing save result
        """
        try:
            from src.interactive.data_state_manager import data_state_manager
            import json
            
            print_info(f"💾 Saving fixed data to original files...")
            
            # Get original data info from state manager
            original_info = data_state_manager.get_loaded_data_info()
            if not original_info:
                return {'status': 'error', 'message': 'No original data information available'}
            
            original_source = original_info.get('source', 'unknown')
            original_path = original_info.get('data_path', '')
            
            print_debug(f"Original source: {original_source}")
            print_debug(f"Original path: {original_path}")
            print_debug(f"Full original info: {original_info}")
            
            # Also try to get source info from the loaded data itself
            loaded_data = data_state_manager.get_loaded_data()
            if loaded_data and isinstance(loaded_data, dict):
                # Look for source_path in DataFrame attributes
                for key, value in loaded_data.items():
                    if hasattr(value, 'attrs') and 'source_path' in value.attrs:
                        source_path = value.attrs['source_path']
                        print_debug(f"Found source_path in {key}: {source_path}")
                        # Update original_path if it was empty
                        if not original_path and source_path:
                            original_path = source_path
                            print_debug(f"Updated original_path from DataFrame: {original_path}")
                        break
            
            # Check if this is an MTF structure (regardless of source name)
            data_type = original_info.get('data_type', '')
            if data_type == 'mtf_structure' or 'mtf_structures' in original_path:
                print_debug(f"Detected MTF structure: {original_path}")
                return self._save_to_mtf_original_files(mtf_data, symbol, original_path)
            
            # Determine save strategy based on original source
            if original_source == 'csv':
                result = self._save_to_csv_original_files(mtf_data, symbol, original_path)
                if result['status'] == 'error':
                    print_warning(f"Failed to save to original CSV files: {result['message']}")
                    print_info(f"Falling back to creating new MTF structure...")
                    return self.save_fixed_data_to_mtf(mtf_data, symbol, 'gaps_fixed')
                return result
            elif original_source == 'raw_parquet':
                result = self._save_to_raw_parquet_original_files(mtf_data, symbol, original_path)
                if result['status'] == 'error':
                    print_warning(f"Failed to save to original raw parquet files: {result['message']}")
                    print_info(f"Falling back to creating new MTF structure...")
                    return self.save_fixed_data_to_mtf(mtf_data, symbol, 'gaps_fixed')
                return result
            elif original_source == 'gaps_fixed':
                return self._save_to_mtf_original_files(mtf_data, symbol, original_path)
            else:
                print_warning(f"Unknown original source: {original_source}")
                print_info(f"Falling back to creating new MTF structure...")
                return self.save_fixed_data_to_mtf(mtf_data, symbol, 'gaps_fixed')
            
        except Exception as e:
            print_error(f"Error saving to original files: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _save_to_csv_original_files(self, mtf_data: Dict[str, Any], symbol: str, original_path: str) -> Dict[str, Any]:
        """Save fixed data to original CSV converted files."""
        try:
            from pathlib import Path
            import json
            
            # Try multiple possible locations for CSV converted files
            possible_dirs = [
                Path("data/cleaned_data/csv_converted"),
                Path("data/cache/csv_converted"),
                Path("data/cleaned_data"),
                Path("data/cache")
            ]
            
            csv_dir = None
            for dir_path in possible_dirs:
                if dir_path.exists():
                    # Check if this directory has files for our symbol
                    symbol_files = list(dir_path.glob(f"*{symbol.lower()}*"))
                    if symbol_files:
                        csv_dir = dir_path
                        print_debug(f"Found CSV files in: {csv_dir}")
                        break
            
            if not csv_dir:
                return {'status': 'error', 'message': f'No original CSV files found for {symbol} in any expected location'}
            
            # Look for symbol files with more specific patterns
            symbol_patterns = [
                f"*{symbol.lower()}*",
                f"*{symbol.upper()}*",
                f"{symbol.lower()}*",
                f"{symbol.upper()}*"
            ]
            
            symbol_files = []
            for pattern in symbol_patterns:
                files = list(csv_dir.glob(pattern))
                symbol_files.extend(files)
            
            # Remove duplicates and filter for parquet files
            symbol_files = list(set([f for f in symbol_files if f.suffix == '.parquet']))
            
            if not symbol_files:
                return {'status': 'error', 'message': f'No original CSV parquet files found for {symbol} in {csv_dir}'}
            
            saved_files = []
            for file_path in symbol_files:
                # Extract timeframe from filename
                timeframe = self._extract_timeframe_from_filename(file_path.name)
                if timeframe and timeframe in mtf_data:
                    # Save fixed data
                    fixed_df = mtf_data[timeframe]
                    fixed_df.to_parquet(file_path)
                    saved_files.append(str(file_path))
                    print_debug(f"Saved {timeframe} to {file_path}")
                else:
                    print_debug(f"Skipped {file_path.name} - timeframe {timeframe} not in mtf_data")
            
            return {
                'status': 'success',
                'symbol': symbol.upper(),
                'source': 'csv',
                'saved_files': saved_files,
                'files_count': len(saved_files),
                'csv_dir': str(csv_dir)
            }
            
        except Exception as e:
            print_error(f"Error saving to CSV files: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _save_to_raw_parquet_original_files(self, mtf_data: Dict[str, Any], symbol: str, original_path: str) -> Dict[str, Any]:
        """Save fixed data to original raw parquet files."""
        try:
            from pathlib import Path
            
            # Try multiple possible locations for raw parquet files
            possible_dirs = [
                Path("data/raw_parquet"),
                Path("data/cleaned_data/raw_parquet"),
                Path("data"),
                Path("data/cleaned_data")
            ]
            
            raw_dir = None
            for dir_path in possible_dirs:
                if dir_path.exists():
                    # Check if this directory has files for our symbol
                    symbol_files = list(dir_path.rglob(f"*{symbol.lower()}*"))
                    if symbol_files:
                        raw_dir = dir_path
                        print_debug(f"Found raw parquet files in: {raw_dir}")
                        break
            
            if not raw_dir:
                return {'status': 'error', 'message': f'No original raw parquet files found for {symbol} in any expected location'}
            
            # Look for symbol files with more specific patterns
            symbol_patterns = [
                f"*{symbol.lower()}*",
                f"*{symbol.upper()}*",
                f"{symbol.lower()}*",
                f"{symbol.upper()}*"
            ]
            
            symbol_files = []
            for pattern in symbol_patterns:
                files = list(raw_dir.rglob(pattern))
                symbol_files.extend(files)
            
            # Remove duplicates and filter for parquet files
            symbol_files = list(set([f for f in symbol_files if f.suffix == '.parquet']))
            
            if not symbol_files:
                return {'status': 'error', 'message': f'No original raw parquet files found for {symbol} in {raw_dir}'}
            
            saved_files = []
            for file_path in symbol_files:
                # Extract timeframe from filename
                timeframe = self._extract_timeframe_from_filename(file_path.name)
                if timeframe and timeframe in mtf_data:
                    # Save fixed data
                    fixed_df = mtf_data[timeframe]
                    fixed_df.to_parquet(file_path)
                    saved_files.append(str(file_path))
                    print_debug(f"Saved {timeframe} to {file_path}")
                else:
                    print_debug(f"Skipped {file_path.name} - timeframe {timeframe} not in mtf_data")
            
            return {
                'status': 'success',
                'symbol': symbol.upper(),
                'source': 'raw_parquet',
                'saved_files': saved_files,
                'files_count': len(saved_files),
                'raw_dir': str(raw_dir)
            }
            
        except Exception as e:
            print_error(f"Error saving to raw parquet files: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _save_to_mtf_original_files(self, mtf_data: Dict[str, Any], symbol: str, original_path: str) -> Dict[str, Any]:
        """Save fixed data to original MTF files."""
        try:
            from pathlib import Path
            import json
            
            # Use original path if available
            if original_path and Path(original_path).exists():
                mtf_dir = Path(original_path)
            else:
                # Fallback to gaps_fixed source
                return self.save_fixed_data_to_mtf(mtf_data, symbol, 'gaps_fixed')
            
            # Update existing MTF files
            main_timeframe = mtf_data.get('_metadata', {}).get('main_timeframe', 'M1')
            
            # Save main data
            main_file = mtf_dir / f"{symbol.lower()}_main_{main_timeframe.lower()}.parquet"
            if main_file.exists() and main_timeframe in mtf_data:
                mtf_data[main_timeframe].to_parquet(main_file)
                print_debug(f"Updated main data: {main_file}")
            
            # Save cross-timeframe data
            cross_dir = mtf_dir / "cross_timeframes"
            if cross_dir.exists():
                for timeframe, df in mtf_data.items():
                    if (isinstance(df, pd.DataFrame) and 
                        not df.empty and 
                        timeframe != main_timeframe and 
                        not timeframe.startswith('_')):
                        
                        cross_file = cross_dir / f"{symbol.lower()}_{timeframe.lower()}_cross.parquet"
                        if cross_file.exists():
                            df.to_parquet(cross_file)
                            print_debug(f"Updated cross timeframe {timeframe}: {cross_file}")
            
            # Update metadata
            metadata_file = mtf_dir / "mtf_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Update metadata with gap fixing info
                metadata.update({
                    'gaps_fixed': True,
                    'last_gap_fix': pd.Timestamp.now().isoformat(),
                    'fixing_strategy': mtf_data.get('_metadata', {}).get('fixing_strategy', 'unknown'),
                    'total_rows': sum(len(df) for df in mtf_data.values() 
                                    if isinstance(df, pd.DataFrame))
                })
                
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2, default=str)
                
                print_debug(f"Updated metadata: {metadata_file}")
            
            return {
                'status': 'success',
                'symbol': symbol.upper(),
                'source': 'mtf_original',
                'mtf_path': str(mtf_dir),
                'files_updated': len(list(mtf_dir.rglob('*.parquet')))
            }
            
        except Exception as e:
            print_error(f"Error saving to MTF original files: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _extract_timeframe_from_filename(self, filename: str) -> Optional[str]:
        """Extract timeframe from filename."""
        try:
            filename_lower = filename.lower()
            if 'm1' in filename_lower:
                return 'M1'
            elif 'm5' in filename_lower:
                return 'M5'
            elif 'm15' in filename_lower:
                return 'M15'
            elif 'm30' in filename_lower:
                return 'M30'
            elif 'h1' in filename_lower:
                return 'H1'
            elif 'h4' in filename_lower:
                return 'H4'
            elif 'd1' in filename_lower:
                return 'D1'
            elif 'w1' in filename_lower:
                return 'W1'
            elif 'mn1' in filename_lower:
                return 'MN1'
            return None
        except Exception:
            return None
    
    def save_fixed_data_to_mtf(self, mtf_data: Dict[str, Any], symbol: str, 
                              source: str = 'gaps_fixed') -> Dict[str, Any]:
        """
        Save fixed data to MTF structure in cleaned_data folder.
        
        Args:
            mtf_data: MTF data structure with fixed data
            symbol: Symbol name
            source: Data source identifier
            
        Returns:
            Dictionary containing save result
        """
        try:
            from pathlib import Path
            import json
            
            print_info(f"💾 Saving fixed data to MTF structure...")
            
            # Create MTF directory structure
            mtf_root = Path("data/cleaned_data/mtf_structures")
            source_dir = mtf_root / source
            source_dir.mkdir(parents=True, exist_ok=True)
            
            symbol_dir = source_dir / symbol.lower()
            symbol_dir.mkdir(parents=True, exist_ok=True)
            
            # Get main timeframe and data
            main_timeframe = mtf_data.get('_metadata', {}).get('main_timeframe', 'M1')
            main_data = mtf_data.get(main_timeframe, pd.DataFrame())
            
            # Save main data
            if not main_data.empty:
                main_file = symbol_dir / f"{symbol.lower()}_main_{main_timeframe.lower()}.parquet"
                main_data.to_parquet(main_file)
                print_debug(f"Saved main data: {main_file}")
            
            # Save cross-timeframe data
            cross_dir = symbol_dir / "cross_timeframes"
            cross_dir.mkdir(exist_ok=True)
            
            cross_timeframes = []
            for timeframe, df in mtf_data.items():
                if (isinstance(df, pd.DataFrame) and 
                    not df.empty and 
                    timeframe != main_timeframe and 
                    not timeframe.startswith('_')):
                    
                    cross_file = cross_dir / f"{symbol.lower()}_{timeframe.lower()}_cross.parquet"
                    df.to_parquet(cross_file)
                    cross_timeframes.append(timeframe)
                    print_debug(f"Saved cross timeframe {timeframe}: {cross_file}")
            
            # Debug: Print information about saved cross timeframes
            print_debug(f"Cross timeframes saved: {cross_timeframes}")
            print_debug(f"Cross timeframes directory: {cross_dir}")
            print_debug(f"Files in cross_timeframes: {list(cross_dir.glob('*.parquet')) if cross_dir.exists() else 'Directory not found'}")
            
            # Create metadata
            metadata = {
                'symbol': symbol.upper(),
                'source': source,  # Add source field
                'main_timeframe': main_timeframe,
                'timeframes': [main_timeframe] + cross_timeframes,
                'total_rows': sum(len(df) for df in mtf_data.values() 
                                if isinstance(df, pd.DataFrame)),
                'main_data_shape': list(main_data.shape) if not main_data.empty else [0, 0],
                'cross_timeframes': cross_timeframes,
                'created_at': pd.Timestamp.now().isoformat(),
                'data_path': str(symbol_dir),
                'main_file': str(main_file) if not main_data.empty else None,
                'gaps_fixed': True,
                'last_gap_fix': mtf_data.get('_metadata', {}).get('last_gap_fix', pd.Timestamp.now().isoformat()),
                'fixing_strategy': mtf_data.get('_metadata', {}).get('fixing_strategy', 'unknown')
            }
            
            # Save metadata
            metadata_file = symbol_dir / "mtf_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            # Create ML loader script
            self._create_ml_loader_script(symbol, metadata, symbol_dir)
            
            print_info(f"✅ Fixed data saved to MTF structure: {symbol_dir}")
            print_info(f"  • Symbol: {symbol.upper()}")
            print_info(f"  • Source: {source}")
            print_info(f"  • Timeframes: {', '.join(metadata['timeframes'])}")
            print_info(f"  • Total rows: {metadata['total_rows']:,}")
            print_info(f"  • Gaps fixed: {metadata['gaps_fixed']}")
            
            return {
                'status': 'success',
                'symbol': symbol.upper(),
                'source': source,
                'mtf_path': str(symbol_dir),
                'metadata': metadata,
                'files_created': len(list(symbol_dir.rglob('*.parquet'))) + 1  # +1 for metadata
            }
            
        except Exception as e:
            print_error(f"Error saving fixed data to MTF: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _create_ml_loader_script(self, symbol: str, metadata: Dict[str, Any], symbol_dir: Path):
        """Create ML loader script for the MTF structure."""
        try:
            script_content = f'''#!/usr/bin/env python3
"""
ML Data Loader for {symbol.upper()} MTF Structure.
Auto-generated script for loading fixed data with gaps filled.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional

class {symbol.upper()}MTFLoader:
    """ML Data Loader for {symbol.upper()} MTF Structure."""
    
    def __init__(self, data_path: str = None):
        """Initialize the loader."""
        if data_path is None:
            data_path = "{symbol_dir}"
        self.data_path = Path(data_path)
        self.metadata = {metadata}
    
    def load_main_data(self) -> pd.DataFrame:
        """Load main timeframe data."""
        main_file = self.data_path / "{symbol.lower()}_main_{metadata['main_timeframe'].lower()}.parquet"
        if main_file.exists():
            return pd.read_parquet(main_file)
        return pd.DataFrame()
    
    def load_cross_timeframe(self, timeframe: str) -> pd.DataFrame:
        """Load cross-timeframe data."""
        cross_file = self.data_path / "cross_timeframes" / "{symbol.lower()}_{{timeframe.lower()}}_cross.parquet"
        if cross_file.exists():
            return pd.read_parquet(cross_file)
        return pd.DataFrame()
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all available data."""
        data = {{}}
        
        # Load main data
        main_data = self.load_main_data()
        if not main_data.empty:
            data['{metadata['main_timeframe']}'] = main_data
        
        # Load cross timeframes
        for tf in {metadata['cross_timeframes']}:
            cross_data = self.load_cross_timeframe(tf)
            if not cross_data.empty:
                data[tf] = cross_data
        
        return data
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get MTF metadata."""
        return self.metadata.copy()

# Example usage
if __name__ == "__main__":
    loader = {symbol.upper()}MTFLoader()
    
    # Load all data
    all_data = loader.load_all_data()
    print(f"Loaded {{len(all_data)}} timeframes")
    
    for tf, df in all_data.items():
        print(f"{{tf}}: {{df.shape}}")
    
    # Get metadata
    metadata = loader.get_metadata()
    print(f"\\nMetadata:")
    print(f"  Symbol: {{metadata['symbol']}}")
    print(f"  Main timeframe: {{metadata['main_timeframe']}}")
    print(f"  Total rows: {{metadata['total_rows']:,}}")
    print(f"  Gaps fixed: {{metadata.get('gaps_fixed', False)}}")
'''
            
            script_file = symbol_dir / f"{symbol.lower()}_ml_loader.py"
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            print_debug(f"Created ML loader script: {script_file}")
            
        except Exception as e:
            print_error(f"Error creating ML loader script: {e}")
