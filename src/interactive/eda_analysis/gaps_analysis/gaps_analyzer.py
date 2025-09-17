# -*- coding: utf-8 -*-
"""
Gaps Analyzer for NeoZork Interactive ML Trading Strategy Development.

This module provides the main interface for gaps analysis and fixing.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime
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
        
        if not loaded_data:
            raise ValueError('No valid timeframe data found in MTF structure')
        
        return loaded_data
    
    def analyze_and_fix_gaps(self, mtf_data: Dict[str, Any], 
                           symbol: str,
                           strategy: str = 'auto',
                           create_backup: bool = True,
                           show_progress: bool = True) -> Dict[str, Any]:
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
            
            # Validate inputs
            if not mtf_data:
                return {'status': 'error', 'message': 'No MTF data provided'}
            
            if strategy not in self.available_strategies:
                return {'status': 'error', 'message': f'Unknown strategy: {strategy}'}
            
            # Create multi-progress tracker
            multi_tracker = MultiProgressTracker(3, f"Gaps Analysis for {symbol}")
            multi_tracker.start()
            
            # Phase 1: Create backup
            backup_result = None
            if create_backup:
                backup_tracker = multi_tracker.start_phase("Backup Creation", 1)
                backup_result = self.backup_manager.create_backup(
                    mtf_data, symbol, "Pre-gap-fixing backup"
                )
                backup_tracker.update(1, "Backup created")
                multi_tracker.finish_phase("Backup Creation", "Backup created successfully")
            
            # Phase 2: Detect gaps
            gaps_tracker = multi_tracker.start_phase("Gaps Detection", 1)
            gaps_result = self._detect_gaps_with_progress(mtf_data, gaps_tracker)
            multi_tracker.finish_phase("Gaps Detection", "Gaps detection completed")
            
            if gaps_result['status'] != 'success':
                return gaps_result
            
            # Phase 3: Fix gaps
            fix_tracker = multi_tracker.start_phase("Gaps Fixing", 1)
            fix_result = self._fix_gaps_with_progress(
                mtf_data, gaps_result, strategy, fix_tracker
            )
            multi_tracker.finish_phase("Gaps Fixing", "Gaps fixing completed")
            
            # Finish all phases
            multi_tracker.finish_all(f"Gaps analysis completed for {symbol}")
            
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
                progress_tracker.update(current, message)
            
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
                progress_tracker.update(current, message)
            
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
