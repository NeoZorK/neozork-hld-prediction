# -*- coding: utf-8 -*-
"""
Indicators MTF Creator for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive MTF (Multi-Timeframe) structure creation
for indicators data with cross-timeframe feature engineering.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import time
import json
from datetime import datetime
import colorama
from colorama import Fore, Style

from src.common.logger import print_error, print_info, print_success, print_warning


class IndicatorsMTFCreator:
    """
    MTF Creator for indicators data.
    
    Provides comprehensive MTF structure creation with cross-timeframe
    feature engineering and ML-optimized data organization.
    """
    
    def __init__(self):
        """Initialize the indicators MTF creator."""
        self.mtf_structures = {}
        self.cross_timeframe_features = {}
        
        # Set up paths
        from pathlib import Path
        self.project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        self.data_root = self.project_root / "data"
        self.cleaned_root = self.data_root / "cleaned_data"
        self.mtf_root = self.cleaned_root / "mtf_structures"
        self.indicators_mtf_root = self.mtf_root / "indicators"
        
        # Ensure directories exist
        self.indicators_mtf_root.mkdir(parents=True, exist_ok=True)
        
    def create_mtf_from_processed_data(self, processed_data: Dict[str, Any], 
                                     symbol: str, main_timeframe: str, 
                                     source: str = 'indicators') -> Dict[str, Any]:
        """
        Create MTF structure from processed indicators data.
        
        Args:
            processed_data: Dictionary containing processed indicators data
            symbol: Symbol name for the MTF structure
            main_timeframe: Main timeframe for the MTF structure
            source: Data source identifier
            
        Returns:
            Dict containing MTF structure with status and metadata
        """
        try:
            print_info(f"🔧 Creating MTF structure for {symbol} indicators...")
            
            start_time = time.time()
            
            # Step 1: Organize data by indicator and timeframe
            organized_data = self._organize_data_by_indicator_and_timeframe(processed_data)
            
            if not organized_data:
                return {
                    'status': 'error',
                    'message': 'No valid data found for MTF structure creation'
                }
            
            # Step 2: Create main MTF data structure
            mtf_data = self._create_main_mtf_structure(organized_data, symbol, main_timeframe, source)
            
            # Step 3: Create cross-timeframe features
            if len(organized_data) > 1:
                print_info("🔄 Creating cross-timeframe features...")
                cross_features = self._create_cross_timeframe_features(organized_data, main_timeframe)
                mtf_data['cross_timeframe_features'] = cross_features
            
            # Step 4: Add metadata and statistics
            mtf_data = self._add_mtf_metadata(mtf_data, processed_data, start_time)
            
            # Step 5: Validate MTF structure
            validation_result = self._validate_mtf_structure(mtf_data)
            if not validation_result['valid']:
                return {
                    'status': 'error',
                    'message': f"MTF structure validation failed: {validation_result['errors']}"
                }
            
            creation_time = time.time() - start_time
            print_success(f"✅ MTF structure created in {creation_time:.2f}s")
            
            return {
                'status': 'success',
                'mtf_data': mtf_data,
                'creation_time': creation_time,
                'metadata': mtf_data['metadata']
            }
            
        except Exception as e:
            print_error(f"Error creating MTF structure: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_mtf_from_single_indicator(self, indicator_data: Dict[str, Any], 
                                       symbol: str, timeframe: str) -> Dict[str, Any]:
        """
        Create MTF structure from single indicator data.
        
        Args:
            indicator_data: Dictionary containing single indicator data
            symbol: Symbol name
            timeframe: Timeframe for the indicator
            
        Returns:
            Dict containing MTF structure
        """
        try:
            print_info(f"🔧 Creating MTF structure for single indicator: {indicator_data.get('indicator', 'Unknown')}")
            
            # Create organized data structure - use filename as key
            organized_data = {
                f"{indicator_data.get('indicator', 'unknown')}_{timeframe}.parquet": indicator_data
            }
            
            # Create MTF structure
            result = self.create_mtf_from_processed_data(organized_data, symbol, timeframe)
            
            return result
            
        except Exception as e:
            print_error(f"Error creating single indicator MTF: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _organize_data_by_indicator_and_timeframe(self, processed_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Organize processed data by indicator and timeframe."""
        try:
            organized_data = {}
            
            for filename, data in processed_data.items():
                indicator = data.get('indicator', 'unknown')
                # Extract timeframe from the data structure
                timeframe = 'unknown'
                if 'timeframe' in data:
                    timeframe = data['timeframe']
                elif 'data' in data and hasattr(data['data'], 'get'):
                    timeframe = data['data'].get('timeframe', 'unknown')
                
                if indicator not in organized_data:
                    organized_data[indicator] = {}
                
                # Store the data directly, not nested
                organized_data[indicator][timeframe] = data
            
            return organized_data
            
        except Exception as e:
            print_error(f"Error organizing data: {e}")
            return {}
    
    def _create_main_mtf_structure(self, organized_data: Dict[str, Dict[str, Any]], 
                                 symbol: str, main_timeframe: str, source: str) -> Dict[str, Any]:
        """Create main MTF data structure."""
        try:
            # Get all indicators and timeframes
            all_indicators = list(organized_data.keys())
            all_timeframes = set()
            
            for indicator_data in organized_data.values():
                all_timeframes.update(indicator_data.keys())
            
            all_timeframes = sorted(list(all_timeframes))
            
            # Create main data structure
            mtf_data = {
                'symbol': symbol.upper(),
                'main_timeframe': main_timeframe,
                'source': source,
                'indicators': all_indicators,
                'timeframes': all_timeframes,
                'indicator_data': organized_data,
                'main_data': pd.DataFrame(),  # Will be populated
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'total_indicators': len(all_indicators),
                    'total_timeframes': len(all_timeframes),
                    'total_rows': 0
                }
            }
            
            # Create main data DataFrame by combining all indicators for main timeframe
            main_dataframes = []
            for indicator, timeframes_data in organized_data.items():
                if main_timeframe in timeframes_data:
                    df = timeframes_data[main_timeframe]['data'].copy()
                    df['indicator'] = indicator
                    main_dataframes.append(df)
            
            if main_dataframes:
                # Combine all indicator data for main timeframe
                main_df = pd.concat(main_dataframes, ignore_index=True)
                
                # Pivot to have indicators as columns
                if 'value' in main_df.columns and 'indicator' in main_df.columns:
                    # Reset index to get timestamp as column if it's in the index
                    if main_df.index.name == 'timestamp' or isinstance(main_df.index, pd.DatetimeIndex):
                        main_df = main_df.reset_index()
                        if 'timestamp' not in main_df.columns:
                            main_df['timestamp'] = main_df.index
                    
                    # Create pivot table with indicators as columns
                    pivot_df = main_df.pivot_table(
                        index='timestamp',
                        columns='indicator',
                        values='value',
                        aggfunc='first'
                    )
                    
                    # Fill NaN values with forward fill
                    pivot_df = pivot_df.ffill()
                    
                    # Add symbol and timeframe columns
                    pivot_df['symbol'] = symbol.upper()
                    pivot_df['timeframe'] = main_timeframe
                    
                    mtf_data['main_data'] = pivot_df
                    mtf_data['metadata']['total_rows'] = len(pivot_df)
            
            return mtf_data
            
        except Exception as e:
            print_error(f"Error creating main MTF structure: {e}")
            return {}
    
    def _create_cross_timeframe_features(self, organized_data: Dict[str, Dict[str, Any]], 
                                       main_timeframe: str) -> Dict[str, Any]:
        """Create cross-timeframe features for ML."""
        try:
            cross_features = {}
            
            # Get all timeframes except main
            all_timeframes = set()
            for indicator_data in organized_data.values():
                all_timeframes.update(indicator_data.keys())
            
            other_timeframes = [tf for tf in all_timeframes if tf != main_timeframe]
            
            for timeframe in other_timeframes:
                timeframe_data = {}
                
                for indicator, timeframes_data in organized_data.items():
                    if timeframe in timeframes_data:
                        df = timeframes_data[timeframe]['data'].copy()
                        
                        # Resample to main timeframe frequency if needed
                        if 'timestamp' in df.columns:
                            df = df.set_index('timestamp')
                        
                        # Create cross-timeframe features
                        if 'value' in df.columns:
                            # Add lagged values
                            for lag in [1, 2, 3, 5, 10]:
                                df[f'{indicator}_{timeframe}_lag_{lag}'] = df['value'].shift(lag)
                            
                            # Add moving averages
                            for window in [5, 10, 20, 50]:
                                df[f'{indicator}_{timeframe}_ma_{window}'] = df['value'].rolling(window=window).mean()
                            
                            # Add volatility measures
                            df[f'{indicator}_{timeframe}_volatility'] = df['value'].rolling(window=20).std()
                            
                            # Add momentum indicators
                            df[f'{indicator}_{timeframe}_momentum'] = df['value'].pct_change()
                            
                            timeframe_data[indicator] = df
                
                if timeframe_data:
                    cross_features[timeframe] = timeframe_data
            
            return cross_features
            
        except Exception as e:
            print_error(f"Error creating cross-timeframe features: {e}")
            return {}
    
    def _add_mtf_metadata(self, mtf_data: Dict[str, Any], processed_data: Dict[str, Any], 
                         start_time: float) -> Dict[str, Any]:
        """Add comprehensive metadata to MTF structure."""
        try:
            # Calculate statistics
            total_rows = mtf_data['metadata']['total_rows']
            total_indicators = len(mtf_data['indicators'])
            total_timeframes = len(mtf_data['timeframes'])
            
            # Calculate data quality metrics
            quality_metrics = self._calculate_data_quality_metrics(mtf_data)
            
            # Add comprehensive metadata
            mtf_data['metadata'].update({
                'creation_time': time.time() - start_time,
                'data_quality': quality_metrics,
                'indicators_list': mtf_data['indicators'],
                'timeframes_list': mtf_data['timeframes'],
                'main_data_shape': mtf_data['main_data'].shape if not mtf_data['main_data'].empty else [0, 0],
                'cross_timeframes_count': len(mtf_data.get('cross_timeframe_features', {})),
                'source_files': list(processed_data.keys()),
                'total_source_files': len(processed_data)
            })
            
            return mtf_data
            
        except Exception as e:
            print_error(f"Error adding MTF metadata: {e}")
            return mtf_data
    
    def _calculate_data_quality_metrics(self, mtf_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate data quality metrics for MTF structure."""
        try:
            metrics = {
                'completeness': 0.0,
                'consistency': 0.0,
                'validity': 0.0,
                'overall_score': 0.0
            }
            
            if mtf_data['main_data'].empty:
                return metrics
            
            df = mtf_data['main_data']
            
            # Completeness: percentage of non-null values
            total_cells = df.size
            non_null_cells = df.count().sum()
            metrics['completeness'] = (non_null_cells / total_cells) * 100 if total_cells > 0 else 0
            
            # Consistency: check for data type consistency
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            metrics['consistency'] = (len(numeric_cols) / len(df.columns)) * 100 if len(df.columns) > 0 else 0
            
            # Validity: check for reasonable value ranges
            if len(numeric_cols) > 0:
                valid_values = 0
                total_values = 0
                
                for col in numeric_cols:
                    col_data = df[col].dropna()
                    if len(col_data) > 0:
                        # Check for reasonable ranges (not all zeros, not all same value)
                        if col_data.nunique() > 1 and not (col_data == 0).all():
                            valid_values += len(col_data)
                        total_values += len(col_data)
                
                metrics['validity'] = (valid_values / total_values) * 100 if total_values > 0 else 0
            
            # Overall score: weighted average
            metrics['overall_score'] = (
                metrics['completeness'] * 0.4 +
                metrics['consistency'] * 0.3 +
                metrics['validity'] * 0.3
            )
            
            return metrics
            
        except Exception as e:
            print_error(f"Error calculating data quality metrics: {e}")
            return {'completeness': 0, 'consistency': 0, 'validity': 0, 'overall_score': 0}
    
    def _validate_mtf_structure(self, mtf_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate MTF structure integrity."""
        try:
            errors = []
            
            # Check required fields
            required_fields = ['symbol', 'main_timeframe', 'indicators', 'timeframes', 'main_data']
            for field in required_fields:
                if field not in mtf_data:
                    errors.append(f"Missing required field: {field}")
            
            # Check main data
            if 'main_data' in mtf_data:
                if mtf_data['main_data'].empty:
                    errors.append("Main data is empty")
                elif len(mtf_data['main_data'].columns) == 0:
                    errors.append("Main data has no columns")
            
            # Check indicators and timeframes consistency
            if 'indicators' in mtf_data and 'timeframes' in mtf_data:
                if not mtf_data['indicators']:
                    errors.append("No indicators found")
                if not mtf_data['timeframes']:
                    errors.append("No timeframes found")
            
            # Check metadata
            if 'metadata' not in mtf_data:
                errors.append("Missing metadata")
            else:
                required_metadata = ['created_at', 'total_indicators', 'total_timeframes']
                for field in required_metadata:
                    if field not in mtf_data['metadata']:
                        errors.append(f"Missing metadata field: {field}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors
            }
            
        except Exception as e:
            print_error(f"Error validating MTF structure: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"]
            }
    
    def save_mtf_structure(self, mtf_data: Dict[str, Any], output_path: Path) -> Dict[str, Any]:
        """Save MTF structure to disk."""
        try:
            print_info(f"💾 Saving MTF structure to {output_path}")
            
            # Create output directory
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Save main data
            if not mtf_data['main_data'].empty:
                main_file = output_path / f"{mtf_data['symbol'].lower()}_main_{mtf_data['main_timeframe'].lower()}.parquet"
                mtf_data['main_data'].to_parquet(main_file)
            
            # Save cross-timeframe features
            if 'cross_timeframe_features' in mtf_data:
                cross_dir = output_path / "cross_timeframes"
                cross_dir.mkdir(exist_ok=True)
                
                for timeframe, features in mtf_data['cross_timeframe_features'].items():
                    for indicator, df in features.items():
                        cross_file = cross_dir / f"{mtf_data['symbol'].lower()}_{timeframe.lower()}_{indicator.lower()}_cross.parquet"
                        df.to_parquet(cross_file)
            
            # Save metadata
            metadata_file = output_path / "mtf_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(mtf_data['metadata'], f, indent=2, default=str)
            
            print_success(f"✅ MTF structure saved successfully")
            
            return {
                'status': 'success',
                'output_path': str(output_path),
                'files_created': len(list(output_path.rglob('*')))
            }
            
        except Exception as e:
            print_error(f"Error saving MTF structure: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_and_save_mtf_structure(self, processed_data: Dict[str, Any], 
                                     symbol: str, main_timeframe: str, 
                                     source: str = 'indicators') -> Dict[str, Any]:
        """
        Create and save MTF structure from processed indicators data.
        
        Args:
            processed_data: Dictionary containing processed indicators data
            symbol: Symbol name for the MTF structure
            main_timeframe: Main timeframe for the MTF structure
            source: Data source identifier
            
        Returns:
            Dict containing MTF structure with status and metadata
        """
        try:
            print_info(f"🔧 Creating and saving MTF structure for {symbol} indicators...")
            
            # Create MTF structure
            mtf_result = self.create_mtf_from_processed_data(processed_data, symbol, main_timeframe, source)
            
            if mtf_result['status'] != 'success':
                return mtf_result
            
            mtf_data = mtf_result['mtf_data']
            
            # Save MTF structure to disk
            symbol_dir = self.indicators_mtf_root / symbol.lower()
            save_result = self.save_mtf_structure(mtf_data, symbol_dir)
            
            if save_result['status'] != 'success':
                return {
                    'status': 'error',
                    'message': f"Failed to save MTF structure: {save_result['message']}"
                }
            
            print_success(f"✅ MTF structure created and saved for {symbol}")
            
            return {
                'status': 'success',
                'mtf_data': mtf_data,
                'save_path': str(symbol_dir),
                'creation_time': mtf_result.get('creation_time', 0),
                'metadata': mtf_data['metadata']
            }
            
        except Exception as e:
            print_error(f"Error creating and saving MTF structure: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_mtf_from_all_indicators(self, indicators_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create MTF structures from all available indicators data.
        
        Args:
            indicators_data: Dictionary containing all indicators data
            
        Returns:
            Dict containing results for all symbols
        """
        try:
            print_info("🔧 Creating MTF structures for all indicators...")
            
            # Group data by symbol
            symbols_data = self._group_data_by_symbol(indicators_data)
            
            if not symbols_data:
                return {
                    'status': 'error',
                    'message': 'No symbol data found for MTF creation'
                }
            
            results = {}
            total_symbols = len(symbols_data)
            
            for i, (symbol, symbol_data) in enumerate(symbols_data.items()):
                print_info(f"📊 Processing symbol {symbol} ({i+1}/{total_symbols})...")
                
                # Determine main timeframe (prefer M1, then M5, etc.)
                timeframes = list(symbol_data.keys())
                timeframe_priority = {'M1': 1, 'M5': 2, 'M15': 3, 'M30': 4, 'H1': 5, 'H4': 6, 'D1': 7, 'W1': 8, 'MN1': 9}
                main_timeframe = min(timeframes, key=lambda x: timeframe_priority.get(x, 999))
                
                # Create MTF structure for this symbol
                mtf_result = self.create_and_save_mtf_structure(
                    symbol_data, symbol, main_timeframe, 'indicators'
                )
                
                results[symbol] = mtf_result
            
            # Calculate overall statistics
            successful = sum(1 for r in results.values() if r['status'] == 'success')
            failed = total_symbols - successful
            
            print_success(f"✅ MTF creation completed: {successful} successful, {failed} failed")
            
            return {
                'status': 'success',
                'results': results,
                'summary': {
                    'total_symbols': total_symbols,
                    'successful': successful,
                    'failed': failed,
                    'success_rate': (successful / total_symbols) * 100 if total_symbols > 0 else 0
                }
            }
            
        except Exception as e:
            print_error(f"Error creating MTF from all indicators: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _group_data_by_symbol(self, indicators_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Group indicators data by symbol."""
        try:
            symbols_data = {}
            
            for filename, data in indicators_data.items():
                # Extract symbol from filename or data
                symbol = self._extract_symbol_from_data(filename, data)
                
                if symbol not in symbols_data:
                    symbols_data[symbol] = {}
                
                # Extract timeframe
                timeframe = data.get('timeframe', 'unknown')
                if timeframe == 'unknown' and 'data' in data:
                    timeframe = data['data'].get('timeframe', 'unknown')
                
                # Store data by symbol and timeframe
                if timeframe not in symbols_data[symbol]:
                    symbols_data[symbol][timeframe] = {}
                
                symbols_data[symbol][timeframe][filename] = data
            
            return symbols_data
            
        except Exception as e:
            print_error(f"Error grouping data by symbol: {e}")
            return {}
    
    def _extract_symbol_from_data(self, filename: str, data: Dict[str, Any]) -> str:
        """Extract symbol from filename or data."""
        try:
            # Try to extract from filename first
            if '_' in filename:
                parts = filename.split('_')
                if len(parts) >= 2:
                    # Look for common symbol patterns
                    for part in parts:
                        if part.upper() in ['BTCUSDT', 'ETHUSDT', 'EURUSD', 'GBPUSD', 'GOOG', 'TSLA', 'US500', 'XAUUSD']:
                            return part.upper()
            
            # Try to extract from data
            if 'symbol' in data:
                return data['symbol'].upper()
            
            if 'data' in data and 'symbol' in data['data']:
                return data['data']['symbol'].upper()
            
            # Default fallback
            return 'UNKNOWN'
            
        except Exception as e:
            print_error(f"Error extracting symbol: {e}")
            return 'UNKNOWN'
